import discord
from discord.ext import commands, tasks
import re
import asyncio
import time



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot_user_id = '410031180163973132'

# Daftar kata-kata terlarang
forbidden_words = ["memek", "kontol", "anjing", "Memek", "Kontol", "Ajing", "ngewe", "Ngewe", "!kontol", "!KONTOL" "!Kontol" "!memek" "!MEMEK" "!memek" "!anjing" "!Anjing" "ANJING"]

# Membuat dictionary untuk melacak pesan pengguna

my_tasks = []

# Dictionary untuk melacak pesan yang dikirim oleh setiap pengguna
user_messages = {}
# ID voice channel yang akan diperbarui
voice_channel_id = 1147134190542917793


# Fungsi untuk menghitung ekspresi matematika yang kompleks
def calculate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f'Error: {str(e)}'
@bot.event
async def on_ready():
    print(f'Bot Sudah Aktif! {bot.user}')
    update_member_count.start()


@bot.event
async def on_member_join(member):
    await update_voice_channel(member.guild)


@tasks.loop(minutes=1)
async def update_member_count():
    for guild in bot.guilds:
        await update_voice_channel(guild)

@update_member_count.before_loop
async def before_update_member_count():
    await bot.wait_until_ready()

async def update_voice_channel(guild):
    # Ganti 'YOUR_VOICE_CHANNEL_ID' dengan ID voice channel yang sesuai
    voice_channel_id = 1147134190542917793  # Ganti dengan ID voice channel Anda

    # Cari voice channel berdasarkan ID
    voice_channel = guild.get_channel(voice_channel_id)

    if voice_channel:
        # Hitung jumlah anggota yang ada di server
        member_count = guild.member_count

        # Mengubah nama voice channel untuk mencantumkan jumlah anggota
        await voice_channel.edit(name=f"Voice Channel ({member_count} Members)")
    else:
        print("Voice channel tidak ditemukan.")


@bot.event
async def on_member_remove(member):
    voice_channel = member.guild.get_channel(voice_channel_id)
    if voice_channel:
        member_count = member.guild.member_count
        await voice_channel.edit(name=f"Voice Channel ({member_count} Members)")
async def on_message(message):
    # Mengabaikan pesan yang dikirim oleh bot sendiri
    if message.author == bot.user:
        return

    if message.content.startswith('pe'):
        await message.channel.send(f'OY {message.author.mention}')

    if message.content.startswith('apakabar'):
        await message.channel.send('Sedikit sakitt..')

    
    if message.content.startswith('author'):
        await message.channel.send(f'Pembuat <@{bot_user_id}>')

    # FILTER KATA KASAR
    content = message.content.lower()  # Mengambil isi pesan dan mengubahnya menjadi huruf kecil
    for word in forbidden_words:
        if word in content:
            await message.delete()  # Menghapus pesan jika mengandung kata terlarang
            await message.channel.send(f"{message.author.mention}, Messages containing forbidden words are not allowed!")
            break

   
     # Pengecualian: Jika pesan dimulai dengan prefix perintah Anda, jangan proses sebagai spam
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return


    # Pengecualian: Jika pesan adalah ulangan dari pesan sebelumnya oleh pengguna yang sama, tetapi tidak dianggap spam jika dimulai dengan prefix
    if content in user_messages and user_messages[content] >= 2 and not content.startswith(bot.command_prefix):
        await message.delete(delay=60)
        await message.channel.send(f"{message.author.mention}, pesan spam tidak diperbolehkan!")
    else:
        # Menambah atau mengupdate pesan dalam dictionary pesan pengguna
        user_messages[content] = user_messages.get(content, 0) + 1

    # Menyimpan waktu pengiriman pesan
    user_message_time = time.time()
    user_messages[message.author.id] = user_messages.get(message.author.id, [])
    user_messages[message.author.id].append(user_message_time)

    # Memeriksa apakah ada pesan spam
    if len(user_messages[message.author.id]) >= 3:
        time_difference = user_message_time - user_messages[message.author.id][0]

        # Jika pesan spam ditemukan dalam waktu singkat, berikan ban
        if time_difference <= 60:  # Mengatur durasi ban dalam detik (60 detik = 1 menit)
            await message.author.ban(reason="Spamming")
            await message.channel.send(f"{message.author.mention} telah diberi ban karena spamming.")
        else:
            # Hapus pesan lama dari daftar jika waktu telah berlalu
            user_messages[message.author.id].pop(0)
    await bot.process_commands(message)




@bot.event
async def on_member_join(member):
    # Membuat pesan selamat datang dengan latar belakang warna
    welcome_embed = discord.Embed(
        title=f"Hey, Welcome, {member.name}!",
        description="Welcome on our servers! 🎉 Please read the rules in #rules and enjoy your time here. Feel free to get acquainted at #introduction.",
        color=0x6554AF
    )

    # Mengirim pesan selamat datang ke channel yang ditentukan
    welcome_channel = member.guild.get_channel(1145015079943802981)  # Ganti dengan ID channel selamat datang Anda
    if welcome_channel is not None:
        await welcome_channel.send(embed=welcome_embed)
    else:
        print("Channel selamat datang tidak ditemukan.")

    # Memberikan peran otomatis kepada anggota baru jika diperlukan
    auto_role = member.guild.get_role(1145172961880461342)  # Ganti dengan ID peran otomatis jika diperlukan
    if auto_role is not None:
        await member.add_roles(auto_role)

    print(f'{member.name} bergabung ke server!')

@bot.command()
async def ban(ctx, member: discord.Member):
    # Melakukan ban pada pengguna dan mengatur durasinya
    await member.ban(reason="Spamming")
    await ctx.send(f"{member.mention} telah diberi ban karena spamming. Durasi ban: 1 menit.")
    
    # Tunggu 1 menit kemudian unbanned pengguna
    await asyncio.sleep(60)
    
    # Unban pengguna
    await member.unban()

@bot.command()
async def meabout(ctx):
    # Membuat pesan embed untuk pesan "meabout"
    embed = discord.Embed(title="Welcome to MeBot", color=0x6554AF)
    embed.add_field(name="Professional Moderation", value="MeBot comes equipped with advanced moderation features to ensure that your server stays clean and safe. From spam checks to filtering out inappropriate language, we're here to protect your community.", inline=False)
    embed.add_field(name="User-Friendly Interface", value="We've designed MeBot with a simple and intuitive interface, allowing you to set up moderation rules with ease, even without any technical expertise.", inline=False)
    embed.add_field(name="Top-notch Security", value="MeBot prioritizes security. We have a robust reporting system, monitor suspicious activities, and enforce rules efficiently.", inline=False)
    embed.add_field(name="Special Features", value="In addition to moderation, we also provide various additional features such as welcome message setups, automatic role systems, and much more to enhance your server members' experience.", inline=False)
    embed.add_field(name="24/7 Support", value="Our team is always ready to assist if you encounter issues or have questions about MeBot. We provide support around the clock.", inline=False)
    embed.set_footer(text="Make your server safer and more comfortable with MeBot. Invite our bot now and experience the difference!")

    # Mengirim pesan embed ke channel yang dipilih
    await ctx.send(embed=embed)

@bot.command()
async def mecreate_event(ctx, judul, tanggal, waktu, tempat, *mentions):
    # Memeriksa apakah ada cukup argumen
    if not (judul and tanggal and waktu and tempat):
        await ctx.send("Format perintah tidak benar. Gunakan: `!buat_acara \"Judul Acara\" \"Tanggal\" \"Waktu\" \"Tempat\" [@mention]`")
        return

    # Menghapus pesan pengguna yang memanggil perintah
    await ctx.message.delete()

    # Menggabungkan semua mention menjadi satu teks
    mention_text = ' '.join(mentions)

    # Membuat pesan embed untuk acara
    embed = discord.Embed(title=f"📅 {judul} 📅", color=0x6554AF)
    embed.add_field(name="Date",    value=tanggal, inline=False)
    embed.add_field(name="Time",    value=waktu, inline=False)
    embed.add_field(name="Place",   value=tempat, inline=False)
    embed.add_field(name="📢 Those mentioned are requested to attend", value=mention_text , inline=False, )

    # Mengirim pesan acara dalam bentuk embed ke channel yang dipilih
    await ctx.send(embed=embed)

@bot.command()
async def mecreate_task(ctx, *, task_text):
    task_texts = task_text.split("|")  # Memisahkan teks tugas dengan "|"
    
    for task_text in task_texts:
        tasks.append({"task": task_text.strip(), "completed": False})

    await ctx.send("Tasks have been created.")


@bot.command()
async def metask_list(ctx, *, title="List of Tasks"):
    embed = discord.Embed(title=title, color=discord.Color.blue())
    
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["completed"] else "❌"
        embed.add_field(name=f"Task {index} {status}", value=task["task"], inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def metask_complated(ctx, task_number: int):
    # Memeriksa apakah nomor tugas valid
    if 1 <= task_number <= len(tasks):
        # Mengubah status checkbox tugas menjadi selesai
        tasks[task_number - 1]["completed"] = True
        await ctx.send("Task marked as completed.")
    else:
        await ctx.send("Task not found.")

@bot.command()
async def metask_edit(ctx, task_number: int, *, new_text):
    # Memeriksa apakah nomor tugas valid
    if 1 <= task_number <= len(tasks):
        # Mengganti teks tugas dengan teks baru
        tasks[task_number - 1]["task"] = new_text
        await ctx.send("Task updated.")
    else:
        await ctx.send("Task not found.")


@bot.command()
async def metask_delete(ctx, *task_numbers):
    if not task_numbers:
        await ctx.send("No tasks specified.")
        return

    deleted_task_count = 0  # Menghitung berapa banyak tugas yang dihapus

    for task_number in task_numbers:
        task_number = int(task_number)
        if 1 <= task_number <= len(tasks):
            # Menghapus tugas dengan nomor yang sesuai
            del tasks[task_number - 1]
            deleted_task_count += 1

    if deleted_task_count > 0:
        await ctx.send(f"{deleted_task_count} task(s) have been deleted.")
    else:
        await ctx.send("No tasks were deleted.")

@bot.command()
async def medelete(ctx, jumlah_pesan: int):
    # Menghapus pesan yang sesuai dengan jumlah yang diminta
    await ctx.channel.purge(limit=jumlah_pesan + 1)  # +1 untuk menghapus pesan perintah


@bot.command()
async def mehi(ctx):
    await ctx.send(f'HI!{ctx.author.mention}');

@bot.command()
async def meloop(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def mearithmeticinfo(ctx):
    await ctx.send(f'Prioritas Aritmatika di Hitung dari Perkalian dan Pembagian Terlebih Dahulu, Jika Perkalian atau Pembagian Sudah Selesai Maka Perjumlahan dan Perkurangan Akan di Esekusi')

@bot.command()
async def mearithmetic(ctx, * , expresion):
    expresion= re.sub(r'[^0-9+\-*/().]', '', expresion)
      # Coba menghitung ekspresi matematika
    result = calculate_expression(expresion)
    
    await ctx.send(f'Result Arithmetic: {result}, {ctx.author.mention}')

@bot.command()
async def mestatus(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'You Status Connection:{latency}ms   {ctx.author.mention} ')
# Ganti 'YOUR_BOT_TOKEN' dengan token bot Anda

@bot.command()
async def meuserinfo(ctx):
    # Mengambil informasi pengguna yang menjalankan perintah
    target_user = ctx.author

    # Membuat pesan embed
    embed = discord.Embed(
        title=f'Informasi Pengguna: {target_user.name}',
        color=0x6554AF
    )
    embed.add_field(name='Nama', value=target_user.name, inline=True)
    embed.add_field(name='Tanggal Bergabung', value=target_user.joined_at.strftime('%Y-%m-%d'), inline=True)
    embed.add_field(name='Peran', value=', '.join([role.name for role in target_user.roles]), inline=False)

    # Mengambil URL avatar pengguna
    if target_user.avatar:
        avatar_url = target_user.avatar.url
    else:
        avatar_url = target_user.default_avatar.url

    embed.set_thumbnail(url=avatar_url)

    # Mengirim pesan embed ke server Discord
    await ctx.send(embed=embed)

@bot.command()
async def mecreate_channel(ctx, channel_name: str):
    # Membuat channel baru
    guild = ctx.guild
    try:
        new_channel = await guild.create_text_channel(channel_name)
        await ctx.send(f'Channel teks baru dengan nama {new_channel.name} telah dibuat!')
    except discord.Forbidden:
        await ctx.send('Bot tidak memiliki izin untuk membuat channel.')

@bot.command()
async def mecreate_voice_channel(ctx, channel_name: str):
    # Membuat channel suara baru
    guild = ctx.guild
    try:
        new_channel = await guild.create_voice_channel(channel_name)
        await ctx.send(f'Channel suara baru dengan nama {new_channel.name} telah dibuat!')
    except discord.Forbidden:
        await ctx.send('Bot tidak memiliki izin untuk membuat channel suara.')

@bot.command()
async def mecreate_category(ctx, category_name: str, text_channel_name: str, voice_channel_name: str):
    # Membuat kategori baru
    guild = ctx.guild
    try:
        category = await guild.create_category(category_name)

        # Membuat channel teks dalam kategori
        text_channel = await guild.create_text_channel(text_channel_name, category=category)

        # Membuat channel suara dalam kategori
        voice_channel = await guild.create_voice_channel(voice_channel_name, category=category)

        await ctx.send(f'Kategori baru dengan nama {category.name} telah dibuat!\n'
                       f'Channel teks baru dengan nama {text_channel.name} telah dibuat!\n'
                       f'Channel suara baru dengan nama {voice_channel.name} telah dibuat!')
    except discord.Forbidden:
        await ctx.send('Bot tidak memiliki izin untuk membuat kategori atau channel.')

@bot.command()
async def mecreate_role(ctx, role_name: str):
    guild = ctx.guild
    try:
        new_role = await guild.create_role(name=role_name)
        await ctx.send(f'Peran baru dengan nama {new_role.name} telah dibuat!')
    except discord.Forbidden:
        await ctx.send('Bot tidak memiliki izin untuk membuat peran.')




@bot.command()
async def memove(ctx, *members: discord.Member):
    # Periksa apakah ada anggota yang ditentukan
    if not members:
        await ctx.send("Tidak ada anggota yang ditentukan untuk dipindahkan.")
        return

    target_channel = ctx.author.voice.channel  # Saluran suara pengguna yang memanggil perintah

    # Periksa apakah pengguna yang memanggil perintah terhubung ke saluran suara
    if target_channel is None:
        await ctx.send("Anda harus terhubung ke saluran suara untuk menggunakan perintah ini.")
        return

    moved_members = []  # Daftar anggota yang berhasil dipindahkan
    failed_members = []  # Daftar anggota yang gagal dipindahkan

    for member in members:
        # Periksa apakah pengguna yang ditentukan terhubung ke saluran suara
        if member.voice is None:
            failed_members.append(member)
        else:
            try:
                await member.move_to(target_channel)
                moved_members.append(member)
            except Exception as e:
                failed_members.append(member)

    if moved_members:
        moved_member_names = ', '.join([member.display_name for member in moved_members])
        await ctx.send(f"Berhasil memindahkan anggota: {moved_member_names} ke {target_channel.name}.")
    if failed_members:
        failed_member_names = ', '.join([member.display_name for member in failed_members])
        await ctx.send(f"Gagal memindahkan anggota: {failed_member_names}.")

    # Kirim pesan ke anggota yang berhasil dipindahkan
    for member in moved_members:
        await member.send(f"Anda telah dipindahkan ke {target_channel.name}.")

@bot.command()
async def medelete_category(ctx, category_name: str):
    # Periksa izin bot untuk menghapus kategori
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Anda tidak memiliki izin untuk menghapus kategori.")
        return

    # Cari kategori berdasarkan nama
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    # Periksa apakah kategori ditemukan
    if category is None:
        await ctx.send(f"Kategori dengan nama '{category_name}' tidak ditemukan.")
        return

    # Hapus kategori beserta semua channel di dalamnya
    await category.delete()
    await ctx.send(f"Kategori '{category_name}' dan semua channel di dalamnya telah dihapus.")

@bot.command()
async def medelete_text_channel(ctx, channel_name: str):
    # Periksa izin bot untuk menghapus channel teks
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("Anda tidak memiliki izin untuk menghapus channel teks.")
        return

    # Cari channel teks berdasarkan nama
    text_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

    # Periksa apakah channel teks ditemukan
    if text_channel is None:
        await ctx.send(f"Channel teks dengan nama '{channel_name}' tidak ditemukan.")
        return

    # Hapus channel teks
    await text_channel.delete()
    await ctx.send(f"Channel teks '{channel_name}' telah dihapus.")

@bot.command()
async def medelete_voice_channel(ctx, channel_name: str):
    # Periksa izin bot untuk menghapus channel suara
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("Anda tidak memiliki izin untuk menghapus channel suara.")
        return

    # Cari channel suara berdasarkan nama
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)

    # Periksa apakah channel suara ditemukan
    if voice_channel is None:
        await ctx.send(f"Channel suara dengan nama '{channel_name}' tidak ditemukan.")
        return

    # Hapus channel suara
    await voice_channel.delete()
    await ctx.send(f"Channel suara '{channel_name}' telah dihapus.")

@bot.command()
async def server_activity(ctx):
    # Mengambil informasi server
    server = ctx.guild
    
    # Menghitung jumlah total anggota di server
    total_members = server.member_count

    # Menghitung jumlah anggota online
    online_members = len([member for member in server.members if member.status == discord.Status.online])

    # Menghitung jumlah anggota yang sedang sibuk (dnd - Do Not Disturb)
    dnd_members = len([member for member in server.members if member.status == discord.Status.dnd])

    # Menghitung jumlah anggota yang sedang away
    idle_members = len([member for member in server.members if member.status == discord.Status.idle])

    # Mengirim informasi aktivitas server ke channel
    await ctx.send(f"Jumlah Anggota Total: {total_members}\n"
                   f"Anggota Online: {online_members}\n"
                   f"Anggota Do Not Disturb: {dnd_members}\n"
                   f"Anggota Idle: {idle_members}")

# Pastikan Anda menjalankan bot Anda dengan perintah 'bot.run(TOKEN)' di akhir kode Anda.


bot.run("MTE0NDg4NjM5OTI5MjY5MDQ4NA.G6gfZm.gi28u6HDb-ISqA1w4rAkNwSYgNvqR8GJSWCX8o")
