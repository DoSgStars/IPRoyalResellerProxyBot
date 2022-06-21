import discord
import os
import requests
import json
import random
import time
import string
import datetime

dt = datetime.datetime.now()
client = discord.Client()
#put your admin id here
admin_id = ""  #admin id here


def randomstring():
    randomstring = "".join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(8))
    return randomstring


@client.event
async def on_ready():
    print('You have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='.help'))


bearer = ""  #iproyal bearer/API key


@client.event
async def on_message(message):
    msg = message.content
    flog = open('log.txt', 'a+')
    flog.write('\n')
    flog.write('{} : {}'.format(dt, msg))
    flog.close
    user = message.author.id
    user = str(user)
    msgauthor = '{}'.format(message.author)
    users = '{0.user}'.format(client)
    bot = 'IPRoyalResellerBot' #Bot name here/ Example IPRoyal#9480
    if msgauthor == users or msgauthor == bot:
        print('were here')
        return
    elif msgauthor != users or msgauthor != bot:
        try:

            with open('webhook.json') as webhookjson:
                data = json.load(webhookjson)

            embed = discord.Embed(description=data['content'],
                                  color=data['color'])
            embed.set_author(name=data['author']['name'])
            embed.set_footer(text="Fall proxies",
                             icon_url="https://i.imgur.com/OWdffBeh.jpg")

            if msg.startswith('hello') or msg.startswith(
                    'Hello') or msg.startswith('Hi') or msg.startswith(
                        'hi') or msg.startswith('Hey') or msg.startswith(
                            'hey'):
                await message.channel.send('Hi!')
                return
            if msg.startswith('.help'):
                await message.channel.send(embed=embed)
                return

            if msg.startswith('.data'):
                x = 0
                print('we are here')
                params = {"search": message.author.id}
                url = "https://dashboard.iproyal.com/api/residential/royal/reseller/sub-users"
                payload = {}
                headers = {'X-Access-Token': 'Bearer {}'.format(bearer)}
                response = requests.get(url,
                                        headers=headers,
                                        data=payload,
                                        params=params)
                users = json.loads(response.content)
                customer_id = message.author.id
                customer_id = str(customer_id)
                while x < len(users['data']):
                    if "{}_{}".format(
                            customer_id,
                            admin_id) in users['data'][x]['username']:
                        userid = str(users['data'][x]['id'])
                        break
                    x += 1
                try:
                    print(userid)
                except Exception:
                    await message.channel.send('``User not registered!``')
                    return
                try:
                    url = "https://dashboard.iproyal.com/api/residential/royal/reseller/sub-users/{}".format(
                        userid)
                    payload = {}
                    headers = {
                        'X-Access-Token': 'Bearer {}'.format(bearer),
                        'Content-Type': 'application/json'
                    }
                    response = requests.request("GET",
                                                url,
                                                headers=headers,
                                                data=payload).text
                    print('yurr')
                    traffic = json.loads(response)
                    #traffic = (person_dict['data'])
                    #print(traffic)
                    dataleft = traffic['availableTraffic']
                    await message.channel.send(
                        'You have {}GB left'.format(dataleft))
                    return
                except Exception as e:
                    flog = open('log.txt', 'a+')
                    flog.write('\n')
                    flog.write('{} : {}'.format(dt, e))
                    flog.close
                    await message.channel.send('error')
                    return
            if msg.startswith('.generate'):
                x = 0
                print('we are here')
                params = {"search": message.author.id}
                url = "https://dashboard.iproyal.com/api/residential/royal/reseller/sub-users"
                payload = {}
                headers = {'X-Access-Token': 'Bearer {}'.format(bearer)}
                response = requests.get(url,
                                        headers=headers,
                                        data=payload,
                                        params=params)
                users = json.loads(response.content)
                customer_id = message.author.id
                customer_id = str(customer_id)
                while x < len(users['data']):
                    if "{}_{}".format(
                            customer_id,
                            admin_id) in users['data'][x]['username']:
                        userid = str(users['data'][x]['id'])
                        userpassword = str(users['data'][x]['password'])
                        break
                    x += 1
                try:
                    print(userid)
                except Exception:
                    await message.channel.send('``User not registered!``')
                    return

                try:
                    username = "{}_{}".format(customer_id, admin_id)
                    country = msg.split()[2].replace(' ', '')
                    what = msg.split()[1].replace(' ', '')
                    amounts = msg.split()[3].replace(' ', '')
                    amount = int(amounts)

                except Exception as e:
                    flog = open('log.txt', 'a+')
                    flog.write('\n')
                    flog.write('{} : {}'.format(dt, e))
                    flog.close
                    await message.channel.send('Error!')
                    await message.channel.send(
                        '.generate (Sticky/Rotating) (Countrycode) (Amount)'
                    )
                    return
                if amount > 3001:
                    await message.channel.send(
                        '``Too many proxies, try less!``')
                    return
                if what == 'sticky':
                    if country == 'us' or country == 'mx' or country == 'cu' or country == 'pr' or country == 'gt' or country == 'ni':
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            #randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                            listee = [
                                '{}:{}:{}:{}_country-{}_session-{}_lifetime-24h'
                                .format(hostname, port, username,
                                        userpassword, country,
                                        randomstring())
                                for _ in range(amount)
                            ]
                            liste = ("\n".join(listee))
                            print(liste)
                            liste_amount = (len(liste))

                            if liste_amount <= 1900:
                                await message.channel.send(liste)
                                return
                            if liste_amount > 1900:
                                f = open("proxies{}.txt".format(amount),
                                         "w+")
                                f.write(liste)
                                f.close()
                                await message.channel.send(
                                    file=discord.File(
                                        'proxies{}.txt'.format(amount)))
                                os.remove("proxies{}.txt".format(amount))
                                return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    if country == 'sg' or country == 'my' or country == 'ph' or country == 'vn' or country == 'id' or country == 'th' or country == "nikeasia":
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            if country == "nikeasia":
                                try:
                                    country = "nikeas"
                                    listee = [
                                        '{}:{}:{}:{}_set-{}_session-{}_lifetime-24h'
                                        .format(hostname, port, username,
                                                userpassword, country,
                                                randomstring())
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                            else:
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_country-{}_session-{}_lifetime-24h'
                                        .format(hostname, port, username,
                                                userpassword, country,
                                                randomstring())
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    if country == 'au' or country == 'nz' or country == 'pg':
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            #randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                            listee = [
                                '{}:{}:{}:{}_country-{}_session-{}_lifetime-24h'
                                .format(hostname, port, username,
                                        userpassword, country,
                                        randomstring())
                                for _ in range(amount)
                            ]
                            liste = ("\n".join(listee))
                            print(liste)
                            liste_amount = (len(liste))

                            if liste_amount <= 1900:
                                await message.channel.send(liste)
                                return
                            if liste_amount > 1900:
                                f = open("proxies{}.txt".format(amount),
                                         "w+")
                                f.write(liste)
                                f.close()
                                await message.channel.send(
                                    file=discord.File(
                                        'proxies{}.txt'.format(amount)))
                                os.remove("proxies{}.txt".format(amount))
                                return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    else:
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            if country == "ftl" or country == "mesh1" or country == "mesh2" or country == "courir":
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_set-{}_session-{}_lifetime-24h'
                                        .format(hostname, port, username,
                                                userpassword, country,
                                                randomstring())
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                            else:
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_country-{}_session-{}_lifetime-24h'
                                        .format(hostname, port, username,
                                                userpassword, country,
                                                randomstring())
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                if what == 'rotating':
                    if country == 'us' or country == 'mx' or country == 'cu' or country == 'pr' or country == 'gt' or country == 'ni':
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            #randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                            listee = [
                                '{}:{}:{}:{}_country-{}'.format(
                                    hostname, port, username, userpassword,
                                    country) for _ in range(amount)
                            ]
                            liste = ("\n".join(listee))
                            print(liste)
                            liste_amount = (len(liste))

                            if liste_amount <= 1900:
                                await message.channel.send(liste)
                                return
                            if liste_amount > 1900:
                                f = open("proxies{}.txt".format(amount),
                                         "w+")
                                f.write(liste)
                                f.close()
                                await message.channel.send(
                                    file=discord.File(
                                        'proxies{}.txt'.format(amount)))
                                os.remove("proxies{}.txt".format(amount))
                                return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    if country == 'sg' or country == 'my' or country == 'ph' or country == 'vn' or country == 'id' or country == 'th' or country == "nikeasia":
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            if country == "nikeasia":
                                try:
                                    country = "nikeas"
                                    listee = [
                                        '{}:{}:{}:{}_set-{}'.format(
                                            hostname, port, username,
                                            userpassword, country)
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                            else:
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_country-{}'.format(
                                            hostname, port, username,
                                            userpassword, country)
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    if country == 'au' or country == 'nz' or country == 'pg':
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            #randomstring = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                            listee = [
                                '{}:{}:{}:{}_country-{}'.format(
                                    hostname, port, username, userpassword,
                                    country) for _ in range(amount)
                            ]
                            liste = ("\n".join(listee))
                            print(liste)
                            liste_amount = (len(liste))

                            if liste_amount <= 1900:
                                await message.channel.send(liste)
                                return
                            if liste_amount > 1900:
                                f = open("proxies{}.txt".format(amount),
                                         "w+")
                                f.write(liste)
                                f.close()
                                await message.channel.send(
                                    file=discord.File(
                                        'proxies{}.txt'.format(amount)))
                                os.remove("proxies{}.txt".format(amount))
                                return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                    else:
                        try:
                            hostname = "geo.iproyal.com"
                            port = "12323"
                            if country == "ftl" or country == "mesh1" or country == "mesh2" or country == "courir":
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_set-{}'.format(
                                            hostname, port, username,
                                            userpassword, country)
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                            else:
                                try:
                                    listee = [
                                        '{}:{}:{}:{}_country-{}'.format(
                                            hostname, port, username,
                                            userpassword, country)
                                        for _ in range(amount)
                                    ]
                                    liste = ("\n".join(listee))
                                    print(liste)
                                    liste_amount = (len(liste))

                                    if liste_amount <= 1900:
                                        await message.channel.send(liste)
                                        return
                                    if liste_amount > 1900:
                                        f = open(
                                            "proxies{}.txt".format(amount),
                                            "w+")
                                        f.write(liste)
                                        f.close()
                                        await message.channel.send(
                                            file=discord.File(
                                                'proxies{}.txt'.format(
                                                    amount)))
                                        os.remove(
                                            "proxies{}.txt".format(amount))
                                        return
                                except Exception as e:
                                    flog = open('log.txt', 'a+')
                                    flog.write('\n')
                                    flog.write('{} : {}'.format(dt, e))
                                    flog.close
                                    await message.channel.send('Error')
                                    return
                        except Exception as e:
                            flog = open('log.txt', 'a+')
                            flog.write('\n')
                            flog.write('{} : {}'.format(dt, e))
                            flog.close
                            await message.channel.send('Error')
                            return
                else:
                    await message.channel.send(
                        "only sticky or rotating is available. Remember to use lowercase letters!"
                    )
                    return
            if msg.startswith('.presets'):
                listee = [
                    'ftl',
                    'mesh1',
                    'mesh2',
                    'Courir',
                    'nikeasia',
                ]
                liste = ("\n".join(listee))
                await message.channel.send(liste)
                return
            if msg.startswith('.countries'):

                url = "https://dashboard.iproyal.com/api/residential/royal/reseller/access/countries"
                payload = {}
                headers = {'X-Access-Token': 'Bearer {}'.format(bearer)}

                response = requests.request("GET",
                                            url,
                                            headers=headers,
                                            data=payload)
                response_text = response.text
                person_dict = json.loads(response_text)
                data = person_dict['countries']
                for element in data:
                    (element['name'])
                for elements in data:
                    (elements['code'])
                a = [element['name'] for element in data]
                b = [elements['code'] for elements in data]
                res = "\n".join("country: {} code: {}".format(x, y)
                                for x, y in zip(a, b))
                f = open("countries.txt", "w+")
                f.write(res)
                f.close()
                await message.channel.send(
                    file=discord.File('countries.txt'))
                os.remove("countries.txt")
                return
            else:
                await message.channel.send(
                    '``Sorry, I dont know this command. Type .help for all commands!``'
                )
                return
        except Exception as e:
            flog = open('log.txt', 'a+')
            flog.write('\n')
            flog.write('{} : {}'.format(dt, e))
            flog.close
            return


#put your token here
client.run(
    '') #Put token in '' and don't change line location
