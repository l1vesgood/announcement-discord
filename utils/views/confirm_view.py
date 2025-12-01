import disnake
from utils.config import config


class ConfirmView(disnake.ui.View):
    def __init__(self, bot, original_message, channel_config, embed):
        super().__init__(timeout=180)
        self.bot = bot
        self.original_message = original_message
        self.channel_config = channel_config
        self.embed = embed

    @disnake.ui.button(label="✉️ Отправить", style=disnake.ButtonStyle.secondary)
    async def send(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        guild = self.bot.get_guild(config.guild_id)
        channel = guild.get_channel(self.channel_config.id)

        if not channel:
            await interaction.response.send_message(
                "Ошибка: Канал не найден.", ephemeral=True
            )
            return

        try:
            msg = await channel.send(embed=self.embed)
            for reaction in self.channel_config.auto_reactions:
                await msg.add_reaction(reaction)

            success_embed = disnake.Embed(
                title="Успешно",
                description="Объявление отправлено!",
                color=disnake.Color.green(),
            )
            await interaction.response.edit_message(
                content=None, embed=success_embed, view=None
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Ошибка при отправке: {e}", ephemeral=True
            )

    @disnake.ui.button(
        label="❌ Отменить отправку", style=disnake.ButtonStyle.secondary
    )
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.response.edit_message(view=None)
