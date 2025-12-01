import disnake
from disnake.ext import commands
import os
from services.database import Database
from utils.config import config
from utils.views.channel_selection import ChannelSelectionView


class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not isinstance(message.channel, disnake.DMChannel):
            return

        if await self.db.is_muted(message.author.id):
            return

        guild = self.bot.get_guild(config.guild_id)
        if not guild:
            print("Guild not found")
            return

        member = guild.get_member(message.author.id)
        if not member:
            try:
                member = await guild.fetch_member(message.author.id)
            except:
                return

        role = guild.get_role(config.player_role_id)
        if role not in member.roles:
            return

        channel_list = []
        for ch in config.channels:
            channel_list.append(f"{ch.emoji} - {ch.name}\n{ch.description}")

        embed = disnake.Embed(
            title="В какой канал вы хотите опубликовать сообщение?",
            description="\n\n".join(channel_list),
        )
        view = ChannelSelectionView(self.bot, message, member)
        await message.channel.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: disnake.Member):
        if await self.db.is_muted(member.id):
            await ctx.send(f"{member.mention} уже в муте.")
            return

        await self.db.mute_user(member.id)
        await ctx.send(f"{member.mention} has been muted from making announcements.")
        try:
            await member.send(
                "Вы были замучены и больше не можете отправлять объявления."
            )
        except disnake.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: disnake.Member):
        if not await self.db.is_muted(member.id):
            await ctx.send(f"{member.mention} не в муте.")
            return

        await self.db.unmute_user(member.id)
        await ctx.send(f"{member.mention} has been unmuted.")
        try:
            await member.send(
                "Вы были размучены и теперь можете отправлять объявления."
            )
        except disnake.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutelist(self, ctx):
        muted_ids = await self.db.get_all_muted()

        if not muted_ids:
            await ctx.send("Нет замученных пользователей.")
            return

        guild = ctx.guild
        muted_users = []
        for user_id in muted_ids:
            member = guild.get_member(user_id)
            if member:
                muted_users.append(f"{member.mention} ({member.name})")
            else:
                muted_users.append(f"<@{user_id}> (ID: {user_id})")

        embed = disnake.Embed(
            title="Список замученных пользователей",
            description="\n".join(muted_users),
            color=disnake.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Announcements(bot))
