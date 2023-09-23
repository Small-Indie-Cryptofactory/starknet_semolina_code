<p align="center">
  <a style="color: blue;" href="#public-software-for-starknet">English</a> / 
  <a style="color: red;" href="#публичный-софт-для-работы-со-starknet">Русский</a>
</p>



# <a id="public-software-for-starknet"></a>🌐🛠️ Public Software for Starknet
<p align="center">Created by <a href="https://t.me/ahillary">Ahillary</a> & <a href="https://t.me/saniksin">Saniksin</a></p>
<p align="center">📱 <a href="https://t.me/python_with_ahillary">Join our Telegram Group</a></p>





### Contents
1. [Installation](#-1-installation)
2. [Configuration](#-2-configuration)
3. [Available Modules](#-3-available-modules)
4. [Wallet Generation](#-4-wallet-generation)
5. [Wallet Deployment](#-5-wallet-deployment)
6. [Free vs Premium version](#6-free-vs-premium-version-)


## 💻 1. Installation
* Clone the repository.
```
git clone git@github.com:Small-Indie-Cryptofactory/starknet_public.git
```

* Install dependencies.

> 📝 **Note**: Windows users may encounter issues when installing the starknet_py SDK. We recommend:
> 
> Following the steps outlined in the <a href="https://starknetpy.readthedocs.io/en/latest/installation.html#windows">official guide</a>.
>
> Following the instructions provided in the <a href="https://sybil-v-zakone.notion.site/sybil-v-zakone/starknet-py-578a3b2fb96e49149a52b987cbbb8c73">community guide</a>.
```
pip install -r requirements.txt
```


* Using the terminal, navigate to the software directory.

* Launch the software.

    * For Windows - ```python app.py```
    * For Linux/MacOS - ```python3 app.py```
    * 

## ⚙ 2. Configuration

* If you have successfully launched the program through **app.py**, another folder named **files** will be created in the project's home directory. It contains the following files: *debug.log, private_keys.csv, proxy.txt, settings.json*. Additionally, the results of the [wallet generation](#-4-wallet-generation) module will be saved in this folder.


* Let's briefly go through the files inside the **files** folder.

    1. ***debug.log***: The main program log. All informational messages from the program that appear in your terminal will be duplicated here.

    2. ***private_keys.csv***: A file where you can specify addresses and private keys for your wallets.

    3. ***proxy.txt***: A file where you can optionally specify proxies if needed.

    4. ***settings.json***: The program's main settings. These include:
   
        - *maximum_gas_price*: The maximum gas price. If the gas price exceeds this parameter, the program will enter "waiting mode" until the gas price drops to the specified level.

        - *node_url*: If you are not using a proxy, you can specify a private node URL (Alchemy/Blast). However, for the proper functioning of the program, we recommend using RPC versions 0.4.0 and higher.

        - *sleep_time*: The time the program waits after each successful action. It is chosen randomly from a range between "from" and "to".

## 🔧 3. Available Modules

Currently, in the __**free version**__, there are 2 modules available:

 * Wallet Generation for Argent, Braavos, Ethereum.
 * Wallet Deployment.
    
    Automatic wallet deploy is supported, compatible with Argent version 0.3.0 and Braavos 000.000.011.

> 📝 **Note**: expansion is planned for the future.
> 

## 🔐 4. Wallet Generation

* After launching the program, in the action selection menu, enter 1 (to choose Generate Ethereum/Argent/Braavos wallet) and press Enter.
* Enter the number of wallets you want the software to create. The number should be a positive integer.
* Enter the name of the wallet you wish to create. There are 3 options available:
    * Argent
    * Braavos
    * Ethereum
* After the wallet generation is complete, they will be available in the **files** folder which will be *automatically created upon program launch*, with the name "argent/braavos/ethereum_current_date_and_time.csv".

## 🚀 5. Wallet Deployment
* After launching the program, in the action selection menu, enter 2 (to choose Deploy Argent & Braavos wallets) and press Enter.
* Next, you have three available options: fill in the file, select an existing one from the list, or specify the full path to your file.
  
   1. If you choose to fill in the file with private keys and addresses, in the **files** folder, which *will be created automatically* after launching the program, locate the file named private_keys.csv. Open it using any CSV editor (we recommend Excel) and fill it out as shown in the example below, then press Enter. Example:
   
        ```
        address, private key <- Mandatory fields! Do not delete!
        0xMyStarknetAddress1, 0xMyPrivateKey1
        0xMyStarknetAddress2, 0xMyPrivateKey2
        0xMyStarknetAddress3, 0xMyPrivateKey3
        ```
    2. If you generated wallets using our [wallet generation](#-4-wallet-generation), you need to enter the number corresponding to the file with private keys and addresses and press Enter.
    3. You also have the option to specify the full path to your file with addresses and private keys. To do this, enter it in the console and press Enter.
   
> 📝 Note: You can mix Argent and Braavos wallets.
    
 * If necessary, in the **files** folder, fill in the proxy file *(proxy.txt) in the format ***username:password@ip:port***. If the number of wallets corresponds to the number of proxies, each wallet will use only one proxy. Otherwise, a proxy will be randomly selected for each wallet. You can leave the proxy.txt file empty. In that case, proxies will not be used! Press Enter to continue.

> 📝 Note: If you do not specify a proxy, the default public node will be used. We do not recommend using it because it is unknown what data it collects and how it may be used in the future. We strongly recommend using private RPC versions 0.4.0 and higher.

* If you have filled everything correctly, the automatic deployment of wallets will begin. The software will determine on its own which provider your wallet belongs to.

* **The wallet balance should be above 0.001 ETH!**
* You can view the action history in the terminal console or in the "files/debug.log" folder.

## 🆚6. Free vs Premium version 🤔
This section provides a detailed comparison between the free and premium versions.

| 🛠 Function                 | 🆓 Free Version | 💎 Premium Version | 📝 Notes                    |
| -------------------------- | :------------: | :----------------: | :-------------------------- |
| 🛠 Wallet Generation        |      ✅        |        ✅           |             -                |
| 🚀 Wallet Deployment        |      ✅        |        ✅           |            -                 |
| ⏫ Wallet Upgrade           |      ❌        |        ✅           | Premium Exclusive           |
| 💵 OKX Withdraw             |      ❌        |        ✅           | Premium Exclusive           |
| 🌉 Official Bridge          |      ❌        |        ✅           | Premium Exclusive           |
| 🔄 Tasks for swaps/liquidity|      ❌        |        ✅           | Available in Premium only   |
| 🔄 Fault Tolerance (Database Usage)|      ❌        |        ✅           | Available in Premium only   |

> 📝 **Note**: Premium features not only include the basics but also offer exclusive functionalities that are not available in the free version. Upgrading to premium gives you access to advanced features and premium support.
---

# <a id="публичный-софт-для-работы-со-starknet"></a>⚙️ Публичный софт для Starknet 🌟
<p align="center">Разработан <a href="https://t.me/ahillary">Ahillary</a> & <a href="https://t.me/saniksin">Saniksin</a></p>
<p align="center">📱 <a href="https://t.me/python_with_ahillary">Присоединяйтесь к нашей Telegram группе</a></p>



### Cодержимое
1. [Установка](#-1-установка)
2. [Настройка](#-2-настройка)
3. [Доступные модули](#-3-доступные-модули)
4. [Генерация кошельков](#-4-генерация-кошельков)
5. [Деплой кошельков](#-5-деплой-кошельков)
6. [Беслатная vs Платная версия](#6-бесплатная-vs-премиум-версия-)


## 💻 1. Установка
* Клонируйте репозиторий.
```
git clone git@github.com:Small-Indie-Cryptofactory/starknet_public.git
```

* Установите зависимости.

> 📝 **Примечание**: Пользователи Windows могут столкнуться с проблемами при установке SDK starknet_py. Мы рекомендуем:
>
> Сделать все по <a href="https://starknetpy.readthedocs.io/en/latest/installation.html#windows">официальному гайду</a>.
>
> Cделать по <a href="https://sybil-v-zakone.notion.site/sybil-v-zakone/starknet-py-578a3b2fb96e49149a52b987cbbb8c73">гайду сообщества</a>.

```
pip install -r requirements.txt
```

* Используя терминал перейдите в директорию софта.

* Запустите софт.
    * для Windows - ```python app.py```
    * для Linux/MacOs - ```python3 app.py```

> 📝 **Примечание**: Если установка прошла успешно, вы автоматически окажетесь в меню выбора действия.

## ⚙ 2. Настройка

* Если вы успешно запустили программу через **app.py** в домашней директории проекта будет создана еще одна папка под названием **files**. Она содержит следующие файлы: *debug.log, private_keys.csv, proxy.txt, settings.json*. Так же, именно в эту папку будет сохраняться результат выполнения модуля [генерации кошельков](#-4-генерация-кошельков).

* Пройдемся коротко по файлам которые находятся внутри папки **files**.
    1. ***debug.log*** - основной лог программы. Сюда будут дублироваться все информационные сообщения программы которые возникают у вас в терминале.
    2. ***private_keys.csv*** - файл в котором вы можете указать адреса и приватные ключи от ваших кошельков. 
    3. ***proxy.txt*** - файл в котором вы по необходимости указываете прокси.
    4. ***settings.json*** - основные настройки программы. К ним относятся:

        - *maximum_gas_price* - максимальная цена газа, если газ будет выше указаного параметра программа будет находится в "режиме ожидания" пока газ не опуститься до соответствующего уровня.
        - *node_url* - если вы не используете прокси, вы можете указать приватный **node url (Alchemy/Blast)**, однако для коректной работы программы мы советуем использовать RPC версии 0.4.0 и выше.
        - *sleep_time* - время ожидания программы после каждого удачного активного действия. Выбирается рандом от (from) до (to).

## 🔧 3. Доступные модули

На текущий момент в __**бесплатной версии**__ доступно 2 модуля:
 * Генерация кошельков Argent, Braavos, Ethereum.
 * Деплой кошельков. 
    
    Автоматический деплой кошельков. Поддержка Argent версии 0.3.0 и Braavos 000.000.011.

    
> 📝 **Примечание**: в будущем планируется расширение

## 🔐 4. Генерация кошельков 

* После запуска программы, в меню выбора действия введите 1 (для выбора Generate wallet Ethereum/Argent/Braavos) и нажмите Enter.
* Введите кол-во кошельков которые софт должен создать. Число должно целым и положительным.
* Введите название кошелька которое хотите создать. Доступно 3 опции:
  * Argent
  * Braavos
  * Ethereum
* После окончания генерации кошельков, они будут доступны в папке **files** *которая будет создана автоматически после запуска программы*, под именем "argent/braavos/ethereum_текущая_дата_и_время.csv"

## 🚀 5. Деплой кошельков

* После запуска программы, в меню выбора действия введите 2 (для выбора Deploy Argent & Braavos wallets) и нажмите Enter.
* Дальше у вас есть 3 доступные опции: заполнить файл, выбрать существующий из списка либо указать полный путь к вашему файлу.
  
  1. Если вы решили заполнить файл с приватными ключами и адресами, в папке **files** которая *будет создана автоматически* после запуска программы найдите файл private_keys.csv, откройте его через любой сsv редактор (мы рекомендуем excel) и заполните его как в примере ниже и нажмите Enter. Пример:

        ```csv
        address, private key <- обязательные поля! Не удаляйте!
        0xMойСтаркнетАдрес1, 0xМойПриватныйКлюч1
        0xMойСтаркнетАдрес2, 0xМойПриватныйКлюч2
        0xMойСтаркнетАдрес3, 0xМойПриватныйКлюч3
        ```

  2. Если вы генерировали кошельки с помощью нашей [генерации кошельков](#-4-генерация-кошельков) вам необходимо ввести цифру, которая соотвествует файлу с приватными ключами и адресами и нажать Enter.
  3. Так же у вас есть возможность указать полный путь к своему файлу с адресами и приватными ключами, для этого введите его в консоль и нажмите Enter.
> 📝 **Примечание**: Вы можете смешивать кошельки Argent и Braavos.


* По надобности в папке **files** заполните файл с прокси *(proxy.txt)* в формате ***логин:пароль@ip:port***. Если количество кошельков будет соответствовать количеству прокси, для каждого кошелька будет использоваться только один прокси. В противном случае, для каждого кошелька прокси будет выбираться рандомно. Вы можете оставить файл *proxy.txt* пустым. В таком случае прокси не будут использоваться! Для продолжения нажмите Enter.

> 📝 **Примечание**: Если вы не укажите прокси, будет использоваться стандартная публичная нода. Мы не рекомендуем ее использовать, по скольку неизвестно какие ваши данные она собирает и как это будет использовать в будущем. Мы настроятельно рекомендуем использовать приватные RPC версии 0.4.0 и выше.
* Если вы все верно заполнили начнется автоматический деплой кошельков. Софт самостоятельно определит к какому провайдеру относится ваш кошелек. 

* **Баланс кошелька должен быть выше 0.001 ETH!**
* Историю действий вы можете увидеть в консоли терминала, либо в папке files/debug.log.

## 🆚6. Бесплатная vs Премиум версия 🤔
В этом разделе подробно рассмотрено различия между бесплатной и премиум версией.

| 🛠 Функция                   | 🆓 Бесплатная версия | 💎 Премиум версия  | 📝 Примечания                |
| --------------------------- | :------------------: | :----------------: | :-------------------------- |
| 🛠 Генерация кошельков       |         ✅           |         ✅          |              -              |
| 🚀 Деплой кошельков          |         ✅           |         ✅          |              -              |
| ⏫ Обновление кошельков      |         ❌           |         ✅          | Эксклюзив для премиума       |
| 💵 OKX Вывод средств        |         ❌           |         ✅          | Эксклюзив для премиума       |
| 🌉 Официальный мост         |         ❌           |         ✅          | Эксклюзив для премиума       |
| 🔄 Задачи для свопов/ликвидности |      ❌           |         ✅          | Доступно только в премиуме   |
| 🛡️ Отказоустойчивость (использование базы данных)|  ❌   |         ✅          | Доступно только в премиуме   |

> 📝 **Примечание**: Премиум функции включают не только базовые возможности, но и предлагают эксклюзивные функциональные возможности, которых нет в бесплатной версии. Переход на премиум версию дает доступ к расширенным функциям и премиум поддержке.
