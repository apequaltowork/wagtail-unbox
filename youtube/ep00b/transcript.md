# Ep 0b — Setting Up Your Machine

Transcript of the narration.

Video: https://www.youtube.com/watch?v=7AtlyySq4l4

No code in this episode.

---

**[0:00]** Setting up your machine.

**[0:04]** Before anything else. If you already have Python three twelve, git, and you know what a virtual environment is, skip this episode. Go straight to episode one. I will see you there.

**[0:18]** For everyone else, this is short. We are installing four things. Python three twelve, an editor, git, and we will get comfortable with a terminal.

**[0:31]** And just as importantly, what we are not installing. No database server. Episodes one to twelve use SQLite, which already ships inside Python. Postgres turns up in episode thirteen and we install it there. And no Node. There is no front end build step in this series, at any point.

**[0:54]** Step one, Python three point twelve. On Windows, use the installer from python.org. On Mac, homebrew. On Debian or Ubuntu, apt &mdash; and note that the venv package is separate there. If you miss it, creating a virtual environment fails later with a confusing error.

**[1:16]** Windows users, this one box causes more failed setups than everything else combined. On the first screen of the installer, tick add python.exe to path. If you already installed without it, run the installer again, choose modify, and tick it then.

**[1:34]** Check it worked. On Windows, p y space minus minus version. On Mac and Linux, python three minus minus version. You want three point twelve something. If it says command not found on Windows, that is the path box.

**[1:53]** Step two, an editor. I use VS Code with the Python extension, and that is what you will see on screen. But any editor works. PyCharm, Neovim, Sublime. Do not spend an afternoon on themes. Install it and move on.

**[2:12]** Step three, git. Windows, use the installer from git-scm.com and accept the defaults. Mac and Linux, one command. Then tell git who you are. You need git because every episode of this series ends on a tag you can check out.

**[2:31]** Step four, and this is the one that matters. A virtual environment is just a folder that holds one project's packages. Without it, every Python project on your machine shares one set of libraries. Two projects that need different versions of Wagtail will fight, and you will lose an evening to it. With one, they never meet.

**[2:54]** Two commands. Make it, then activate it. On Mac and Linux the activate command is slightly different, and it is on screen now.

**[3:05]** Look at your prompt. It now starts with .venv in brackets. That prefix is the whole lesson. It means you are inside the environment.

**[3:16]** Here is the trap. Opening a new terminal window starts you outside the environment again. You have to activate every single time. This is the number one reason that, three episodes from now, a command suddenly cannot find Wagtail. Nothing broke. You are just outside the venv.

**[3:38]** One more Windows thing. If activate fails saying running scripts is disabled on this system, that is PowerShell's execution policy. Run the command on screen, answer yes, and try again. It only affects your own user account.

**[3:55]** Let us check everyone is in the same place. Three commands. Python, git, and venv support. If all three run without an error, you are ready.

**[4:08]** Notice we have not installed Wagtail at all. That is deliberate. It is the first command of episode one. Delete the practice folder, because the real project starts from an empty directory. And if anything failed, leave a comment with your operating system and the exact error text.

**[4:28]** Next episode, we install Wagtail, create a project, and log into a real CMS admin. And then we stop, and read every single file it generated.

**[4:41]** That is your starting line. Next episode, we install Wagtail.
