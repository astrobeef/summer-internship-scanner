# Install Process
1. I installed the package in the local environment: `python -m pip install playwright`
2. I then installed the headless browser (stored in AppData/Local/ms-playwright): `playwright install`

# Need
While working on the Activision fetch process, I found that cookies and tokens were required for using the API. Geting these automatically is quite a complex process which requires spoofing a browser. That's out of the scope of things I want to spend time on for this project, so I'm using the package [playwright](https://pypi.org/project/playwright/).

I take that back. I thought cookies/tokens would be needed. But as a last check, I tried fetching the API without cookies or a token and I got a response. So I'm removing playwright.

At least now I know how to solve this issue if it comes up later.

# Uinstall Process
1. Remove headless browser: `playwright uninstall`
2. Remove package: `python -m pip uninstall playwright`