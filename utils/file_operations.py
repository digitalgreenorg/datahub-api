from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import logging, os, shutil, cssutils, re

from .validators import validate_image_type

LOGGER = logging.getLogger(__name__)


def delete_directory(directory: str):
    """
    Remove the file path or destination directory with all the files & directories under it.

    **Parameters**
    ``destination`` (str): directory or file path
    """
    try:
        if not os.path.exists(directory):
            LOGGER.error(f"{directory} not found")
            raise FileNotFoundError(f"{directory} not found")
        else:
            shutil.rmtree(directory)
            LOGGER.info(f"Deleting directory: {directory}")
    except Exception as error:
        LOGGER.error(error, exc_info=True)


def remove_files(file_key: str, destination: str):
    """
    Remove files from the file path or destination directory.

    **Parameters**
    ``file_key`` (str): file name or file name without extension
    ``destination`` (str): directory or file path
    """
    try:
        # destination = rf"{destination}" + "/"
        fs = FileSystemStorage(destination)
        with os.scandir(destination) as file_path:
            for file in file_path:
                # deleting file based on file key, that is passed without extension
                if file.is_file() and file.name.split(".")[:-1][0] == file_key:
                    LOGGER.info(f"Deleting file: {destination+file.name}")
                    fs.delete(destination + file.name)
                # deleting file based on file name
                elif file.is_file() and file.name == file_key:
                    LOGGER.info(f"Deleting file: {destination+file.name}")
                    fs.delete(destination + file.name)
    except Exception as error:
        LOGGER.error(error, exc_info=True)


def create_directory(destination: str):
    """
    Create a directory at the destination or skip if exists.

    **Parameters**
    ``directory`` (str): directory name
    """
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
            LOGGER.info(f"Creating directory: {destination}")
    except Exception as error:
        LOGGER.error(error, exc_info=True)
    return destination


def file_save(source_file, file_name: str, directory: str):
    """
    Save or replace files at the preferred destination or file path.

    **Parameters**
    ``source_file`` (file obj): file obj to be saved
    ``file_name`` (str): file name to be saved
    ``destination`` (str): directory or file path where to save the file
    """

    try:
        fs = FileSystemStorage(directory)
        fs.save(directory+ file_name, source_file)
        LOGGER.info(f"File saved: {directory+file_name}")
    except Exception as error:
        LOGGER.error(error, exc_info=True)
    return file_name

def file_path(destination: str):
    """
    Return file paths and its file names without file extensions.

    **Parameters**
    ``destination`` (str): directory or file path

    **Returns**
    ``file_paths`` (dict): dictionary containing file names & file paths

        ``Example``
        {'key': 'path/to/file.ext'}
    """
    try:
        file_paths = {
            os.path.splitext(os.path.basename(file))[0]: destination + file.name
            for file in os.scandir(destination)
        }
        LOGGER.info(f"file paths: {file_paths}")
        return file_paths
    except Exception as error:
        LOGGER.error(error, exc_info=True)


def files_move(source: str, destination: str):
    """
    Move files from location to another on the file system.

    **Parameters**
    ``source`` (str): source directory or file path from where the file needs to be moved
    ``destination`` (str): directory or file path where to where the file needs to be saved
    """
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)  # create directory

        for source_file in os.scandir(source):
            if source_file.is_file():
                with open(destination + source_file.name, "wb+") as dest_file:
                    # shutil.copyfileobj(source+source_file.name, destination)
                    shutil.copy(source + source_file.name, destination)
                    remove_files(source_file.name, source)
                    LOGGER.info(f"file moved: {source+source_file.name}")

    except Exception as error:
        LOGGER.error(error, exc_info=True)


def file_rename(file: str, key: str):
    """
    Returns the desired file name for a file.

    **Parameters**
    ``file_name`` (str): file_name to be converted
    ``key`` (str): key for the file name

    **Returns**
    ``file_name`` (str): desired file name
    """
    try:
        validate_image_type(file)
        file_split = str(file).split(".")

        if not key:
            timestamp = str(timezone.now().timestamp())
            file_to_save = file_split[:-1][0] + "-" + timestamp + "." + file_split[-1]
        elif key:
            file_to_save = key + "." + file_split[-1]
        return file_to_save

    except Exception as error:
        LOGGER.error(error, exc_info=True)


def get_css_attributes(css_path: str, css_attribute: str):
    """
    Returns CSS attribute value of the HTML element.

    **Parameters**
    ``css_path`` (str): CSS file path
    ``css_attribute`` (str): CSS property or attribute

    **Returns**
    ``css_attribute_value`` (str): value of CSS attribute or property
    """
    try:
        with open(css_path) as css:
            sheet = cssutils.css.CSSStyleSheet()
            sheet.cssText = css.read()
            css_attribute_value = sheet.cssRules[0].style[css_attribute]
        return css_attribute_value
    except Exception as error:
        LOGGER.error(error, exc_info=True)
