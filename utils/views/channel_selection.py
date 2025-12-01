import disnake
from utils.config import config


class ChannelSelectionView(disnake.ui.View):
    def __init__(self, bot, original_message, member):
        super().__init__(timeout=180)
        self.bot = bot
        self.original_message = original_message
        self.member = member

        has_text = bool(original_message.content)
        has_image = bool(original_message.attachments)

        msg_type = None
        if has_text and has_image:
            msg_type = "both"
        elif has_text:
            msg_type = "text"
        elif has_image:
            msg_type = "image"

        if not msg_type:
            return

        for channel_config in config.channels:
            supported = channel_config.format
            is_supported = False

            if isinstance(supported, str):
                if supported == msg_type:
                    is_supported = True
            elif isinstance(supported, list):
                if msg_type in supported:
                    is_supported = True

            if is_supported:
                from utils.views.channel_button import ChannelButton

                self.add_item(
                    ChannelButton(channel_config, bot, original_message, member)
                )
