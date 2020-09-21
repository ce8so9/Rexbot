import discord
import time
from discord.ext import commands


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Kick members

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(title='**USER KICKED**',description=f'User **{member}** has been kicked due to:\n **{reason}**', colour=0xff0000)
                await ctx.send(embed=embed)
                kick_embed = discord.Embed(title=f'You have been kicked from {member.guild.name} server', description=f'You have been kicked from the server **{member.guild.name}** for **{reason}**', colour=0xff0000)
                kick_embed.set_thumbnail(url=member.guild.icon_url)
                await member.send(embed=kick_embed)
            except Exception as e:
                await ctx.send(f"I do not have sufficient privelages to kick **{str(member)}**")
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await ctx.send(embed=embed)
            if channel is not None:
                author = ctx.author.id
                emb = discord.Embed(title='Illegal use of command **kick**', description=f'<@{author}> Used the `kick` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)

 
    # Kick members: Error handling

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send('```\n$kick {member_name} {reason}\n      ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **kick**', description=f'<@{author}> Used the `kick` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send('Member not found!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **kick**', description=f'<@{author}> Used the `kick` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        else:
            await ctx.send(f'**{error}**')


    # Ban members

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        
        if ctx.message.author.guild_permissions.ban_members:
            try:
                if reason is None:
                    await ctx.send("What is the reason for the ban?")
                else:
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{member}** has been banned due to:\n **{reason}**', colour=0xff0000)
                    await ctx.send(embed=embed)
                    ban_embed = discord.Embed(title=f'You have been banned from {member.guild.name} server', description=f'You have been banned from the server **{member.guild.name}** for **{reason}**', colour=0xff0000)
                    ban_embed.set_thumbnail(url=member.guild.icon_url)
                    await member.send(embed=ban_embed)

                    await member.ban(reason=reason)
            except:
                await ctx.send(f"I dont have sufficient privelages to ban {str(member)}!")        
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await channel
            if channel is not None:
                author = ctx.author.id
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'`<@{author}>` Used the `ban` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Ban members: Error handling

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send('```\n$ban {member_name} {reason}\n     ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'<@{author}> Used the `ban` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.message.author.guild_permissions.ban_members:
                await ctx.send('Member was not found!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'<@{author}> Used the `ban` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        else:
            await ctx.send(f'**{error}**')


    # Unban members

    @commands.command()
    async def unban(self, ctx, *, member):
        try:
            if ctx.message.author.guild_permissions.ban_members:
                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = member.split('#')

                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)
                        embed = discord.Embed(description=f'***Unbanned user {user.mention}***', colour=0x008000)
                        await ctx.send(embed=embed)
                        return
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id.mention
                    emb = discord.Embed(title='Illegal use of command **unban**', description=f'`<@{author}>` Used the `unban` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        except ValueError:
            await ctx.send("Too few arguments\nSyntax: `$unban <username>#<discriminator>`")
        except Exception as e:
            print(f'{e}')


    # Unban mambers: Error handling
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("Too few arguments\nSyntax: `$unban <username>#<discriminator>`")
        else:
            await ctx.send(f'**{error}**')
                
    
    # Clear command
    
    @commands.command(aliases=['remove','purge'])
    async def clear(self, ctx, amount=0):
        if ctx.message.author.guild_permissions.manage_messages:
            if amount == 0:
                await ctx.send("How many do you want to remove?")
            else:
                await ctx.channel.purge(limit=amount + 1)
                time.sleep(0.5)
                msg = await ctx.send(f"Removed {amount} messages!")
                time.sleep(1.5)
                await msg.delete()
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await channel
            if channel is not None:
                author = ctx.author.id
                emb = discord.Embed(title='Illegal use of command **clear**', description=f'`<@{author}>` Used the `clear` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Announcements

    @commands.command()
    async def userpost(self, ctx, *, message=None):
        try:
            if ctx.message.author.guild_permissions.manage_messages:
                if message is None:
                    await ctx.send("What is the message?")
                else:
                    channel = discord.utils.get(ctx.guild.channels, name='general')
                    await channel.send(message)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **userpost**', description=f'`<@{author}>` Used the `userpost` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
                    
        except Exception as e:
            await ctx.send(f"Some weird error bot is mad about {e}")


    # Embeded Announcements

    @commands.command()
    async def embedpost(self, ctx, *, message=None):
        if ctx.message.author.guild_permissions.manage_messages:
            if message is None:
                await ctx.send("What is the message to send")
            else:
                channel = discord.utils.get(ctx.guild.channels, name='general')
                embed = discord.Embed(title=f'Announcement by **{ctx.message.author}**', description=f'*{message}*', colour=0x0000ff)
                await channel.send(embed=embed)
        else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **embedpost**', description=f'`<@{author}>` Used the `embedpost` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
                    

    # Mute members

    @commands.command(aliases=['mute'])
    async def _mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if str(member.name) == str(ctx.author.name):
                await ctx.send(f"**You can't mute yourself {ctx.author.mention}**")
            else:
                if reason is None:
                    await ctx.send("What is the reason for the mute?")
                else:
                    mute_role_exist = True
                    is_user_muted = False

                    muted1 = discord.utils.get(ctx.guild.roles, name='Muted')

                    for role in member.roles:
                        if role.id == muted1.id:
                            is_user_muted = True
                        else:
                            is_user_muted = False

                    if mute_role_exist:
                        if is_user_muted:
                            embed = discord.Embed(title='Already muted', description=f'**{member.name}** is already muted!', colour=0xf86000)
                            await ctx.send(embed=embed)
                        else:
                            await member.add_roles(muted1)
                            emb = discord.Embed(title=f'You have been muted in {member.guild.name}', description=f'You have been muted in **{ctx.guild.name}** server for **{reason}**', colour=0xff0000)
                            embed = discord.Embed(title='User muted!', description=f'**{member}** was muted by **{ctx.message.author}** for:\n\n**{reason}**', colour=0xff0000)
                            await ctx.send(embed=embed)
                            await member.send(embed=emb)
                    else:
                        embed = discord.Embed(title='ERROR', description=f'Mute role does not exist in this server!\n I cannot mute {member.mention}', colour=0xff0000)
                        await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await channel
            if channel is not None:
                author = ctx.author.id
                emb = discord.Embed(title='Illegal use of command **mute**', description=f'<@{author}> Used the `mute` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Mute member: Error handling

    @_mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('```\n$mute {member_name}\n      ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'<@{author}> Used the `mute` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('Member does not exist!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'<@{author}> Used the `mute` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        else:
            await ctx.send(f'**{error}**')
                
    

    # Unmute member

    @commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(member.roles, name='Muted')
            if role is not None:
                await member.remove_roles(role)
                embed = discord.Embed(title='User unmuted!', description='**{0}** was unmuted by **{1}**\n\nDon\'t be naughty again'.format(member, ctx.message.author), colour=0x008000)
                await ctx.send(embed=embed)
                emb = discord.Embed(title='Unmuted', description=f'You have been unmuted from the server **{member.guild.name}**\nDon\'t be naughty again', colour=0x008000)
                await member.send(embed=emb)
            else:
                embed = discord.Embed(
                    title = 'User not muted',
                    description = f'{member.mention} is not muted!',
                    colour=0xf86000
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await channel
            if channel is not None:
                author = ctx.author.id
                emb = discord.Embed(title='Illegal use of command **unmute**', description=f'<@{author}> Used the `unmute` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Unmute member : Error handling

    @_unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('```\n$unmute {member_name}\n        ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **unmute**', description=f'<@{author}> Used the `unmute` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('The user does not exist!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await channel
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **unmute**', description=f'<@{author}> Used the `unmute` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
                

    # Adding roles

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, *, role=None):
        try:
            if ctx.message.author.guild_permissions.manage_roles:
                if role is None:
                    await ctx.send(f"Which role do you want to give to **{str(member)}**? ")
                if member is None:
                    await ctx.send(f'Please enter a valid member\nMember **{str(member)}** does not exist')
                else:
                    add_role = discord.utils.get(ctx.guild.roles, name=role)
                    if add_role is not None:
                        await member.add_roles(add_role)
                        embed = discord.Embed(title='**ADDED ROLE**', description=f'**{str(member)}** has been given the role **{role}**', colour=0x008000)
                        await ctx.send(embed=embed)
                    elif role is None:
                        pass
                    else:
                        await ctx.send(f'the role **{role}** does not exist!\n**NOTE:** the addrole command is **case sensitive**')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'<@{author}> Used the `addrole` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        except Exception as e:
            await ctx.send(f'Bot is mad about **{e}**')

    
    # Add roles: Error handling

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('```\n$addrole {member_name} {role}\n         ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'<@{author}> Used the `addrole` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send(f'Member not found!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'<@{author}> Used the `addrole` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)

        else:
            await ctx.send(f'**{error}**')
                
    

    # Remove roles

    @commands.command(aliases=['removerole'])
    async def purgerole(self, ctx, member: discord.Member, *, role=None):
        try:
            if ctx.message.author.guild_permissions.manage_roles:
                if role is None:
                    await ctx.send(f"Which role do you want to remove from **{str(member)}**? ")
                else:
                    add_role = discord.utils.get(ctx.guild.roles, name=role)
                    if add_role is not None:
                        await member.remove_roles(add_role)
                        embed = discord.Embed(title='**REMOVED ROLE**', description=f'Remved **{role}** from user **{str(member)}**', colour=0x008000)
                        await ctx.send(embed=embed)
                    elif role is None:
                        pass
                    else:
                        await ctx.send(f'Role **{role}** does not exist!\n**NOTE**: the removerole/purgerole command is **case sensitive**')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **removerole**', description=f'<@{author}> Used the `removerole` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)
        except Exception as e:
            await ctx.send(f'Bot is mad about **{e}**')
                
    
    # Remove roles: Error handling

    @purgerole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.send('```\n$removerole {member_name} {role}\n            ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **removerole**', description=f'<@{author}> Used the `removerole` command, Who is not a moderator', colour=0xff0000)
                    await channel.semd(embed=embed)

        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send(f'Member not found!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    author = ctx.author.id
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'<@{author}> Used the `addrole` command, Who is not a moderator', colour=0xff0000)
                    await channel.send(embed=emb)

        else:
            await ctx.send(f'**{error}**')
                    
    

def setup(bot):
    bot.add_cog(ModerationCog(bot))
