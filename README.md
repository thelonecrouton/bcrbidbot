# bcrbidbot

PyQT GUI bot for scheduled Electrum BTC payments, targeted towards bidding for Bitcredit (BCR)


Instructions:

1. Install Electrum BTC wallet. See https://electrum.org for details. 
2. Start Electrum and uncheck Use Change Addresses under Tools > Preferences, so you don't have to keep importing new BTC privkeys into your BCR wallet, just one initially.
3. Backup, then fund your electrum wallet.
4. Under the Addresses tab in Electrum, right click on the funded address, select Privkey, enter your password and cut and paste this somewhere.
5. Start your BCR wallet and import the BTC privkey. Do this by clicking the Debug Window icon along the bottom of the wallet, selecting the Console tab, and first entering 'walletpassphrase yourpassphrase 60' to unlock the wallet, 
followed by 'importprivkey privkey'. 
6. Start bcrbidbot with 'python bcrbidbot.py' or whatever is appropriate for your OS.
7. You can select either a one-off bid or an everyday bid at a specified time.
8. When you have entered your preferences, click Bid!
