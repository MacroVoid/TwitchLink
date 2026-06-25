import sys
from chat_downloader.sites.twitch import TwitchChatDownloader
from chat_downloader.cli import main

# Patch the Twitch Client-ID
TwitchChatDownloader._CLIENT_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

# Update the hashes to the latest known ones (StreamMetadata and VideoMetadata changed)
TwitchChatDownloader._OPERATION_HASHES.update({
    'StreamMetadata': 'b57f9b910f8cd1a4659d894fe7550ccc81ec9052c01e438b290fd66a040b9b93',
    'VideoMetadata': '45111672eea2e507f8ba44d101a61862f9c56b11dee09a15634cb75cb9b9084d',
})

# Monkey-patch _download_gql to add new required variables like includeIsDJ
original_download_gql = TwitchChatDownloader._download_gql

def patched_download_gql(self, ops):
    if isinstance(ops, list):
        for op in ops:
            if op.get('operationName') == 'StreamMetadata':
                if 'variables' not in op:
                    op['variables'] = {}
                op['variables']['includeIsDJ'] = False
    return original_download_gql(self, ops)

TwitchChatDownloader._download_gql = patched_download_gql

if __name__ == '__main__':
    sys.exit(main())
