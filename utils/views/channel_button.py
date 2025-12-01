import disnake


class ChannelButton(disnake.ui.Button):
    def __init__(self, channel_config, bot, original_message, member):
        super().__init__(
            label=f"{channel_config.emoji} {channel_config.name}",
            style=disnake.ButtonStyle.secondary,
        )
        self.channel_config = channel_config
        self.bot = bot
        self.original_message = original_message
        self.member = member

    async def callback(self, interaction: disnake.MessageInteraction):
        from utils.config import config

        channel_list = []
        for ch in config.channels:
            channel_list.append(f"{ch.emoji} - {ch.name}\n{ch.description}")

        main_embed = disnake.Embed(
            title="В какой канал вы хотите опубликовать сообщение?",
            description="\n\n".join(channel_list)
        )

        rules_embed = disnake.Embed(
            title=f"Правила канала {self.channel_config.name}",
            description=self.channel_config.rules
        )

        from utils.views.rules_view import RulesView

        view = RulesView(
            self.bot, self.original_message, self.channel_config, self.member
        )
        await interaction.response.edit_message(
            content=None, embeds=[main_embed, rules_embed], view=view
        )
