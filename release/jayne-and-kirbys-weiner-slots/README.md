# Jayne & Kirby's Weiner Slots

A self-contained three-reel wiener dog slot machine. Five paylines, autoplay,
a progressive Wiener Jackpot (three **Cash** symbols on the middle line), and
seven very long dogs. Play money only — no accounts, purchases, or real-money
gambling.

Everything is in `index.html`; there are no external libraries, fonts, or build
tools. The Cash jackpot symbol is the `cashmoney.jpg` photo, cropped and inlined
as a data URI, so the page still makes no image requests. Progress is saved in
the browser with `localStorage`.

## Play on this computer

```bash
cd pickle-slots
python3 app.py
```

Open the printed URL (default: <http://localhost:8000>). If port 8000 is busy:

```bash
PORT=8080 python3 app.py
```

`app.py` binds to all network interfaces by default so a phone on the same
Wi-Fi can also connect. To keep it local only: `HOST=127.0.0.1 python3 app.py`.

## Play on a phone on the same Wi-Fi

1. Run `python3 app.py` on the computer.
2. Connect the phone to the same Wi-Fi network.
3. Open the **On a phone** URL printed by the server, for example
   `http://192.168.1.42:8000`.
4. If it will not connect, allow Python through the computer's firewall for
   private networks.

The LAN URL is plain HTTP, so the game plays fine but cannot be installed as a
home-screen app. For that, use an HTTPS host below.

## Put it on the web (free)

The folder is already a finished static site. No build command is needed.

### Easiest: Netlify Drop

1. Go to <https://app.netlify.com/drop>.
2. Drag this folder (the one containing `index.html`) onto the page.
3. Netlify returns a public `https://…` address. Open it on a phone.
4. iPhone: Share → **Add to Home Screen**. Android: menu → **Install app**.

### Other static hosts

Upload the contents of the release folder to Cloudflare Pages, GitHub Pages,
Vercel, Firebase Hosting, or any static web host. Publish directory: the folder
itself. No framework, runtime, or server code is required.

## Send it as one file

`release/Jayne-and-Kirbys-Weiner-Slots.html` is a standalone copy. Send it by
email or chat and open it in a browser. Some phone messaging apps refuse to run
local HTML attachments, so a hosted link is more reliable for phones.

## Installable app / offline play

When served over HTTPS, the game registers a service worker and caches itself.
After the first load it opens without a connection and can be installed to the
home screen. The service worker is skipped automatically when the HTML file is
opened directly from disk.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole game (HTML, CSS, Canvas art, JavaScript) |
| `manifest.webmanifest` | Home-screen name, colours, and icons |
| `sw.js` | Offline cache |
| `icons/` | App icons, including maskable and Apple touch icons |
| `app.py` | Optional local/LAN static server |
| `_headers` | Header hints for Netlify/Cloudflare Pages |

## Controls

- **Spin** button or `Space`
- Bet: `↑` / `↓` or `+` / `−`
- Autoplay 10 spins: `A` or the Auto button
- Mute: `M`
- Reset balance, jackpot, and stats: click **reset game** twice

The 5% jackpot contribution is separate from the 93.4% base line-pay RTP shown
in the footer.
