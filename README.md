# gmadget
A tool for getting steam workshop collections downloaded locally.

## Usage

Download the tool (hit 'Download Zip' button).
Then extract and run console_here.bat

That should open a shiny console window for you.

Now type, for example, for the workshop url (http://steamcommunity.com/sharedfiles/filedetails/?id=619946236):

gmadget --singleids 619946236

That will download the workshop item and extract it in the gmadget folder, under the name of the addon :).

There is also

gmadget --collectionid (collection id)

that does the same thing for collections.

## Troubleshooting

The tool, at first run, tries to guess where the gmad.exe file is. If this fails, edit or gmad_path_best_guess.txt with the path to gmad.exe :)
And, if you can arse, create a support issue or email magnusjjj@gmail.com :)