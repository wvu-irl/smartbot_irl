from pathlib import Path

from smartbot_irl.utils.smart_logging import SmartLogger, logging
from ..data._data_logging import timestamp
from ..data import State
import sys

logger = SmartLogger(level=logging.WARN)  # Print statements, but better!


def get_log_dir(log_dir_name='smart_logs') -> Path:
    script_dir = Path(sys.argv[0]).resolve().parent
    log_dir = script_dir.parent / log_dir_name
    log_dir.mkdir(exist_ok=True)
    return log_dir


def save_data(states: State, params, log_filename='smart') -> Path:
    # Path of dir containing main script.
    script_dir = Path(sys.argv[0]).resolve().parent

    # Path to save csv in.
    log_dir = script_dir.parent / 'smart_data'
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / (log_filename + f'_{timestamp()}.csv')

    states.to_csv(log_path)
    logger.info(f'Saved data in {log_path}')

    return log_path
