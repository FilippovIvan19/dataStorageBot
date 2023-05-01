from telebot.types import BotCommand
from enum import Enum

ROOT_DIR_NAME = 'root'

# /commands
HELP_COMMAND = 'help'
ROOT_COMMAND = 'root'
LAST_ACTIVE_DIR_COMMAND = 'last_active_dir'
SEARCH_COMMAND = 'search'
TAGS_COMMAND = 'tags'

# keyboard buttons
CREATE_SUBDIR_BTN_TEXT = 'create subdir'
UPLOAD_FILE_BTN_TEXT = 'upload file'

# inline keyboard
DIRECTORY_VIEW_SCOPE = 'dir'
FILE_VIEW_SCOPE = 'file'
TAG_VIEW_SCOPE = 'tag'

NAVIGATION_OPTION = 'nav'
FILE_OPEN_OPTION = 'file'
ADD_OPTION = 'add'
EDIT_OPTION = 'edit'
DELETE_OPTION = 'delete'
ATTACH_OPTION = 'attach'
DETACH_OPTION = 'detach'

DIRECTORY_EMOJI = '\N{open file folder}'
AUDIO_EMOJI = '\N{musical note}'
DOCUMENT_EMOJI = '\N{page facing up}'
PHOTO_EMOJI = '\N{sunrise over mountains}'
VIDEO_EMOJI = '\N{clapper board}'
TAG_EMOJI = '\N{bookmark}'
ADD_EMOJI = '\N{squared new}'
EDIT_EMOJI = '\N{pencil}'
DELETE_EMOJI = '\N{cross mark}'

# hints
MY_COMMANDS = [
    BotCommand(HELP_COMMAND, 'get bot usage prompts'),
    BotCommand(ROOT_COMMAND, f'open directory \"{ROOT_DIR_NAME}\"'),
    BotCommand(LAST_ACTIVE_DIR_COMMAND, 'open last active directory'),
    BotCommand(SEARCH_COMMAND, 'search files by tags'),
    BotCommand(TAGS_COMMAND, 'view and edit tags'),
]

HELP_TEXT = f"""\
Use /{HELP_COMMAND} command to see this guide
Use /{ROOT_COMMAND} command to open directory \"{ROOT_DIR_NAME}\"
Use /{LAST_ACTIVE_DIR_COMMAND} command to open directory you visited latest
Use /{SEARCH_COMMAND} command to execute search in file system based on tags attached to files
Use /{TAGS_COMMAND} command to view and edit tags list 
"""


# supported file types
class FileTypes(Enum):
    AUDIO = 'audio'
    DOCUMENT = 'document'
    PHOTO = 'photo'
    VIDEO = 'video'
