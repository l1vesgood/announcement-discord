import disnake
from utils.skins import check_bust


class RulesView(disnake.ui.View):
    def __init__(self, bot, original_message, channel_config, member):
        super().__init__(timeout=180)
        self.bot = bot
        self.original_message = original_message
        self.channel_config = channel_config
        self.member = member

    @disnake.ui.button(label="✅ Согласиться", style=disnake.ButtonStyle.secondary)
    async def agree(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        embed = disnake.Embed(description=self.original_message.content or None)
        if self.original_message.attachments:
            embed.set_image(url=self.original_message.attachments[0].url)

        nickname = self.member.display_name
        skin_url = await check_bust(nickname)

        if skin_url:
            embed.set_author(name=nickname, icon_url=skin_url)
        else:
            embed.set_author(
                name=nickname, icon_url=self.original_message.author.display_avatar.url
            )

        if self.channel_config.contacts:
            embed.add_field(
                name="Контакты:",
                value=f"{self.member.mention} ({self.member.name})",
                inline=False,
            )

        preview_embed = disnake.Embed(
            title="Опубликовать сообщение?",
            description=f"Ваше сообщение будет сразу опубликовано в канал: {self.channel_config.emoji}{self.channel_config.name}",
        )

        from utils.views.confirm_view import ConfirmView

        view = ConfirmView(self.bot, self.original_message, self.channel_config, embed)
        await interaction.response.edit_message(
            content=None, embeds=[preview_embed, embed], view=view
        )

    @disnake.ui.button(
        label="❌ Отменить отправку", style=disnake.ButtonStyle.secondary
    )
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.response.edit_message(view=None)
