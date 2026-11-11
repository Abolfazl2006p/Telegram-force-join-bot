# Telegram Force Join Bot

A Telegram bot built with Python and the requests library. This bot requires users to join a specific private channel before they can use its features.

## Features
- Inline Keyboards: Interactive buttons for user navigation.
- Force Join Mechanism: Validates user membership in a private channel using the Telegram API (getChatMember).
- Proxy Support: Built-in support for passing local proxies (useful for bypassing network restrictions).
- No Heavy Frameworks: Uses only the requests library for lightweight performance.

## Setup
1. Install the required library:
   `bash
   pip install requests