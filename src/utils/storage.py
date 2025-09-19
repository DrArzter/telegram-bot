import json
import os
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

ADS_FILE = "ads.json"


def load_ads() -> List[Dict[str, Any]]:
    """
    Loads advertisements from JSON file.

    Returns:
        List[Dict[str, Any]]: Loaded advertisements
    """
    if not os.path.exists(ADS_FILE):
        logger.info(f"File {ADS_FILE} not found, creating empty list")
        return []

    try:
        with open(ADS_FILE, "r", encoding="utf-8") as f:
            ads = json.load(f)
            logger.info(f"Loaded {len(ads)} ads from {ADS_FILE}")
            return ads
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading ads: {e}")
        return []


def save_ads(ads: List[Dict[str, Any]]) -> bool:
    """
    Saves advertisements to JSON file.

    Args:
        ads: Advertisements list

    Returns:
        bool: True if the advertisements were saved successfully
    """
    try:
        with open(ADS_FILE, "w", encoding="utf-8") as f:
            json.dump(ads, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(ads)} ads to {ADS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving ads: {e}")
        return False


def add_ad(
    user_id: int, ad_type: str, content: str = "", file_id: str = "", caption: str = ""
) -> bool:
    """
    Creates a new advertisement and adds it to the list.

    Args:
        user_id: User ID
        ad_type: Advertisement type (text, photo, audio, voice)
        content: Text content
        file_id: File media ID
        caption: Media description

    Returns:
        bool: True if the advertisement was added successfully
    """
    ads = load_ads()

    new_ad = {"id": len(ads) + 1, "user_id": user_id, "type": ad_type, "likes": 0}

    if ad_type == "text":
        new_ad["content"] = content
    elif ad_type in ["photo", "audio", "voice"]:
        new_ad["file_id"] = file_id
        if caption:
            new_ad["caption"] = caption

    ads.append(new_ad)
    result = save_ads(ads)

    if result:
        logger.info(f"Added new {ad_type} ad for user {user_id}")

    return result


def get_user_ads(user_id: int) -> List[Dict[str, Any]]:
    """
    Returns a list of advertisements for a user.

    Args:
        user_id: User ID

    Returns:
        List[Dict[str, Any]]: User's advertisements
    """
    ads = load_ads()
    user_ads = [ad for ad in ads if ad["user_id"] == user_id]
    logger.info(f"Found {len(user_ads)} ads for user {user_id}")
    return user_ads


def delete_ad(ad_id: int, user_id: int) -> bool:
    """
    Deletes an advertisement from the list.

    Args:
        ad_id: Advertisement ID
        user_id: User ID

    Returns:
        bool: True if the advertisement was deleted successfully
    """
    ads = load_ads()

    for i, ad in enumerate(ads):
        if ad["id"] == ad_id and ad["user_id"] == user_id:
            deleted_ad = ads.pop(i)
            result = save_ads(ads)
            if result:
                logger.info(f"Deleted ad {ad_id} by user {user_id}")
            return result

    logger.warning(f"Ad {ad_id} not found or user {user_id} is not the owner")
    return False


def like_ad(ad_id: int, user_id: int) -> tuple[bool, str]:
    """
    Adds like to advertisement if user hasn't liked it yet.

    Args:
        ad_id: Advertisement ID
        user_id: User ID who is liking

    Returns:
        tuple[bool, str]: (Success status, Message)
    """
    ads = load_ads()

    for ad in ads:
        if ad["id"] == ad_id:
            if "liked_by" not in ad:
                ad["liked_by"] = []

            if user_id in ad["liked_by"]:
                return False, "You already liked this advertisement"

            ad["liked_by"].append(user_id)
            ad["likes"] = len(ad["liked_by"])

            result = save_ads(ads)
            if result:
                logger.info(
                    f"User {user_id} liked ad {ad_id}, total likes: {ad['likes']}"
                )
                return True, f"Liked! Total likes: {ad['likes']}"
            else:
                return False, "Failed to save like"

    logger.warning(f"Ad {ad_id} not found for liking")
    return False, "Advertisement not found"


def get_ad_by_id(ad_id: int) -> Optional[Dict[str, Any]]:
    """
    Returns advertisement by ID.

    Args:
        ad_id: Advertisement ID

    Returns:
        Optional[Dict[str, Any]]: Advertisement or None
    """
    ads = load_ads()

    for ad in ads:
        if ad["id"] == ad_id:
            return ad

    return None
