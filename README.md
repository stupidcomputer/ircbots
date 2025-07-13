# ircbots
Back in the long long ago(tm), I wrote a crap ton of stupid IRC bots.
This is a collection of all of them, which used to be stored in individual repositories, crammed into one repository.

Here are all of them, in no particular order:
- [botanybot](./botanybot) -- on various machines in the [tildeverse](https://tildeverse.org), there was a little game called botany, in which you had to log in and water your plants. [tilde.team](https://tilde.team) had a bot that allowed you to water your plants via IRC, but [tilde.club](https://tilde.club) did not. this bot was written to fill that gap.
- [pychaos](./pychaos) -- on the tilde.chat irc network there was a channel called #chaos where everyone got +o and a bunch of other privileges. this bot (well, really, a series of bots) protected me in case I was kicked, and kickbanned anyone who tried to kick me.
- [coinminer](./coinminer) -- there was a bot called tildebot that allowed you to wager imaginary coins on the results of a coin flip. this bot brute-forced this by repeatedly exploiting the beginner coin bonus and sending it to my main account.
- [modbot](./modbot) -- a generic modular irc robot. the module system isn't that good, looking back. it certainly was an achievement back then.
- [chaosbot](./chaosbot) -- my first irc robot, based on a hacked up version of a little irc client called `ii`. terrible c programming ahead!
- [universalducks](./universalducks) -- after ~100 messages, there was a bot that sent a message that a duck was loose. the first person to get the duck won the duck. this bot is the same, except it operates over many channels in parallel; that is, there is one duck to be captured over many channels.

# License
All these projects are licensed under their respective licenses. In the case where there is no license, the files therein are licensed under the [AGPL](./LICENSE.md).

All code in this repo, unless otherwise noted, is (c) 2018-2025 stupidcomputer and licensed under the respective licenses therein.
