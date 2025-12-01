import aiohttp
import logging

logger = logging.getLogger(__name__)


async def check_bust(nickname: str):
    url = f"https://visage.surgeplay.com/bust/256/{nickname}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True, headers=headers) as resp:
                if resp.status == 200:
                    return url
                else:
                    return None
    except Exception as e:
        logger.error(f"Error checking skin for {nickname}: {e}")
        return None
