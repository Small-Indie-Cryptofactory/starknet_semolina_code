<p align="center">
  <a style="color: blue;" href="#public-software-for-starknet">English</a> / 
  <a style="color: red;" href="#публичный-софт-для-работы-со-starknet">Русский</a>
</p>



# <a id="public-software-for-starknet"></a>🌐🛠️ Public Software for Starknet
<p align="center">Created by <a href="https://t.me/ahillary">Ahillary</a> & <a href="https://t.me/saniksin">Saniksin</a></p>
<p align="center">📱 <a href="https://t.me/python_with_ahillary">Join our Telegram Group</a></p>
<p align="center">📺 <a href="https://add.link">Video Tutorial on Software Usage</a></p>




### Contents
1. [Installation](#-1-installation)
2. [Available Modules](#-2-available-modules)
3. [Wallet Generation](#-3-wallet-generation)
4. [Wallet Deployment](#-4-wallet-deployment)
5. [Free vs Premium version](#5-free-vs-premium-version-)


## 💻 1. Installation
* Clone the repository.
```
git clone ...
```

* Install dependencies.

```
pip install -r requirements.txt
```
> 📝 **Note**: On Windows, there may be installation issues with the starknet_py SDK. We recommend:

> Following the steps outlined in the <a href="https://starknetpy.readthedocs.io/en/latest/installation.html#windows">official guide</a>.

> Following the instructions provided in the <a href="https://sybil-v-zakone.notion.site/sybil-v-zakone/starknet-py-578a3b2fb96e49149a52b987cbbb8c73">community guide</a>.

* Using the terminal, navigate to the software directory.

* Launch the software.

    * For Windows - ```python app.py```
    * For Linux/MacOS - ```python3 app.py```

## 🔧 2. Available Modules

Currently, in the __**free version**__, there are 2 modules available:

 * Wallet Generation for Argent, Braavos, Ethereum.
 * Wallet Deployment.
    
    Automatic wallet deploy is supported, compatible with Argent version 0.3.0 and Braavos 000.000.011.

> 📝 **Note**: expansion is planned for the future.

## 🔐 3. Wallet Generation

* In the action selection menu, choose option 1 and press Enter.

* Enter the number of wallets you want the software to create. The number should be a positive integer.
* Enter the name of the wallet you wish to create. There are 3 options available:
    * Argent
    * Braavos
    * Ethereum

## 🚀 4. Wallet Deployment
* In the action selection menu, choose option 2 and press Enter.
* Fill in the file where you need to specify wallets in the format: address, private key. 
    
    For example:
```
address, private key
0xMyStarknetAddress1, 0xMyPrivateKey1
0xMyStarknetAddress2, 0xMyPrivateKey2
0xMyStarknetAddress3, 0xMyPrivateKey3
```
> 📝 **Note**: you can mix Argent and Braavos wallets.

* If necessary, fill in the proxy file in the format http://username:password@ip:port and specify the path to it.

> 📝 **Note**: If you don't specify a proxy, the standard public node will be used. We do not recommend using it, as it is unclear what data it collects and how it will be used in the future. We strongly recommend using private RPC versions 0.4.0 and above.

* If you have filled everything correctly, automatic wallet deployment will begin. The software will determine on its own which provider your wallet belongs to.

## 🆚5. Free vs Premium version 🤔
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
<p align="center">📺 <a href="https://add.link">Видео обзор по использованию софта</a></p>


### Cодержимое
1. [Установка](#-1-установка)
2. [Доступные модули](#-2-доступные-модули)
3. [Генерация кошельков](#-3-генерация-кошельков)
4. [Деплой кошельков](#-4-деплой-кошельков)
5. [Беслатная vs Платная версия](#5-бесплатная-vs-премиум-версия-)


## 💻 1. Установка
* Клонируйте репозиторий.
```
git clone ...
```

* Установите зависимости.
```
pip install -r requirements.txt
```
> 📝 **Примечание**: на Windows может возникать проблема с установкой starknet_py SDK. Мы рекомендуем:

> Сделать все по <a href="https://starknetpy.readthedocs.io/en/latest/installation.html#windows">официальному гайду</a>.

> Cделать по <a href="https://sybil-v-zakone.notion.site/sybil-v-zakone/starknet-py-578a3b2fb96e49149a52b987cbbb8c73">гайду сообщества</a>.

* Используя терминал перейдите в директорию софта.

* Запустите софт.
    * для Windows - ```python app.py```
    * для Linux/MacOs - ```python3 app.py```

> 📝 **Примечание**: Если установка прошла успешно, вы автоматически окажетесь в меню выбора действия.

## 🔧 2. Доступные модули

На текущий момент в __**бесплатной версии**__ доступно 2 модуля:
 * Генерация кошельков Argent, Braavos, Ethereum.
 * Деплой кошельков. 
    
    Автоматический деплой кошельков. Поддержка Argent версии 0.3.0 и Braavos 000.000.011.

    
> 📝 **Примечание**: в будущем планируется расширение

## 🔐 3. Генерация кошельков 

* В меню выбора действия выберете 1 и нажмите Enter.
* Введите кол-во кошельков которые софт должен создать. Число должно целым и положительным.
* Введите название кошелька которое хотите создать. Доступно 3 опции:
  * Argent
  * Braavos
  * Ethereum

## 🚀 4. Деплой кошельков

* В меню выбора действия выберете 2 и нажмите Enter.
* Заполните файл в котором нужно указать кошельки в формате:
    address, private key.

Пример:
```csv
address, private key
0xMойСтаркнетАдрес1, 0xМойПриватныйКлюч1
0xMойСтаркнетАдрес2, 0xМойПриватныйКлюч2
0xMойСтаркнетАдрес3, 0xМойПриватныйКлюч3
```
> 📝 **Примечание**: Вы можете смешивать кошельки Argent и Braavos.
  
* По надобности заполните файл с прокси в формате http://логин:пароль@ip:port и укажите путь к нему.

> 📝 **Примечание**: если вы не укажите прокси, будет использоваться стандартная публичная нода. Мы не очень рекомендуем ее использовать, по скольку неизветсно какие ваши данные она собирает и как это будет использовать в будущем. Мы настроятельно рекомендуем использовать приватные RPC версии 0.4.0 и выше.
* Если вы все верно заполнили начнется автоматический деплой кошельков. Софт самостоятельно определит к какому провайдеру относится ваш кошелек.

## 🆚5. Бесплатная vs Премиум версия 🤔
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
