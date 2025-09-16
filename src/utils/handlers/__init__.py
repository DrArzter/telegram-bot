from aiogram import Dispatcher
import importlib
import pkgutil
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

def include_routers(dp: Dispatcher) -> None:
    """
    Includes all routers from the handlers directory into the given dispatcher.

    :param dp: The dispatcher to include routers into.
    :type dp: Dispatcher
    """
    handlers_path = Path(__file__).parent
    
    for _, module_name, _ in pkgutil.iter_modules([str(handlers_path)]):
        if module_name == '__init__':
            continue
        try:
            module = importlib.import_module(f".{module_name}", package=__name__)
            if hasattr(module, "router"):
                dp.include_router(module.router)
                logger.info(f"Router from {module_name} included successfully")
        except Exception as e:
            logger.error(f"Error importing {module_name}: {e}")
