---
layout: archive
title: "Citation Style Language files"
permalink: /csl/
author_profile: true
---

##Custom Citation Style Language for outreach librarianship
Project abstract (originally written for a conference proposal): _Many librarians that do outreach work either do not use or do not have access to their ILS systems, making creating book lists for displays or purchase requests tedious. However, there is an innovative approach to rapidly generating book lists from both the open web and library catalogs. By creating a custom Citation Style Language compatible with Zotero, librarians can quickly save and export book lists with relevant metadata such as call numbers or ISBNs. By using generative AI and Citation Style Language’s code editor, functional workflow requirements can be integrated into custom CSL code without programming expertise. Harnessing the power of open-source platforms like Zotero and the Citation Style Language project alongside generative artificial intelligence allows librarians doing outreach work to streamline their workflows._

The custom citation style that I created to allow me to use Zotero to create book lists is called Librarian Utility Style. There are two variations, Librarian Utility Style - Pull List w/ Call Numbers and Librarian Utility Style - Purchase Request. These two styles cover the two scenerios in which I am creating book lists: creating a list of books to be pulled from the shelf for a display and creating a list of books that I would like our acquisitions team to purchase. 

###Librarian Utility Style - Pull List w/ Call Numbers
[Download CSL file here](_pages/librarian-utility-style-pull-list-w-call-numbers.csl)
###Librarian Utility Style - Book Request List
[Download CSL file here](_pages/librarian-utility-style-purchase-requests.csl)
When I downloaded, I was prompted to install the style in Zotero. However, if you are not prompted here are the instructions provided by [Visual CSL Editor](https://editor.citationstyles.org/visualEditor/)
**Zotero**
Go to "Preferences...", "Cite", "Styles", click the "+" button and select the downloaded style.
**Paperpile**
Go to "Settings > Citation Styles > Custom styles", click the "Upload CSL file" button and select the downloaded CSL file. The newly added citation style will be listed in the "Custom styles" section on successful upload.
**Mendeley**
You can use [Mendeley's own version of this CSL Editor](http://csl.mendeley.com), where Mendeley will host your style, install it directly to your computer and help you share the style with other CSL users.

Once you do that you will be able to export a bibliography in Librarian Utility Style - Pull List w/ Call Numbers.
Example:
Z721 .C22 2013. _The library: a world history._ Campbell, J.W.P. 2013.

User note: When using Librarian Utility Style - Pull List w/ Call Numbers to save a book that is not in the general collection, add the name of the collection to the "Extra" metadata field. It will place the collection name before the call number and all items with something in the Extra field will be listed first. 
Example:
JUV. PZ7.B9832 Pe 2011. _Penelope Popper, book doctor._ Buzzeo, T. 2011.
