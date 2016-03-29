# bcrbidbot

PyQT GUI bot for scheduled Electrum BTC payments, targeted towards bidding for Bitcredit (BCR)

Dependencies:
sudo pip install pexpect

Instructions:

1. Install Electrum BTC wallet. See https://electrum.org for details. 
2. Start Electrum and uncheck Use Change Addresses under Tools > Preferences, so you don't have to keep importing new BTC privkeys into your BCR wallet, just one initially.
3. Backup, then fund your electrum wallet.
4. Under the Addresses tab in Electrum, right click on the funded address, select Privkey, enter your password and cut and paste this somewhere.
5. Close Electrum, then restart it in daemon mode with 'electrum daemon start' - then forget about it and leave it running.
6. Start your BCR wallet and import the BTC privkey. Do this by clicking the Debug Window icon along the bottom of the wallet, selecting the Console tab, and first entering 'walletpassphrase yourpassphrase 60' to unlock the wallet, 
followed by 'importprivkey privkey'. 
7. Start bcrbidbot with 'python bcrbidbot.py' or whatever is appropriate for your OS.
8. You can select either a one-off bid or an everyday bid at a specified time.
9. When you have entered your preferences, click Bid!
10. You can change your scheduled bid time/amount, just click Bid! again afterwards to queue the new bid.

IMPORTANT NOTE: 

bcrbidbot will attemp to send the BTC amount THAT IS IN THE AMOUNT FIELD AT THE TIME THE BID IS MADE. So if you schedule a bid of 0.1 BTC, but later change that amount in the entry box to 10 BTC before the bid is made, 10 BTC is what will get bid! Future versions might 'lock' the bid at the amount in the box at the time the bid button is clicked, this version DOES NOT.

License

bcrbidbot is released under the terms of the MIT license. For more information see http://opensource.org/licenses/MIT.


Copyright (c) 2016 thelonecrouton
