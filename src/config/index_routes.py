from fastapi.responses import RedirectResponse


async def docs(): return RedirectResponse(url="/docs")