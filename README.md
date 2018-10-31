# Bioload

#### Author: Vasco Varas

___

 **Pre-requisites:**

- Python3
- PIP3
- MySQL and user (with auth_plugin: mysql_native_password) Follow the [link](https://github.com/Vasco-Varas/Bioload/blob/master/installmysql.md) for the tutorial.

**Description:** Bioload takes your CD-HIT virome protein clustering results and generates a tab-delimited table linking proteins in your dataset with Tara virome protein clusters (TOV) and their metadata. Bioload can help you classify your own proteins into Tara Ocean Virome protein clusters as in [Brum *et al*. 2015](http://science.sciencemag.org/content/348/6237/1261498).

**Expected line:** `python3 bioload.py <Tara file> <infofile> [CD-HIT output...]`

**Help:**

- `<Tara file>` The file where the Tara Protein clusters are located.
- `<infofile>` The infofile.txt included with the program. This file contains the metadata from the Tara Ocean samples, e.g., location, physicochemical properties, depth, biogeographical region, etc. The file should be tab delimited.
- `[CD-HIT output...]` The CD-HIT output  (You can give it 2 or more files separated by spaces).

**Example line:** `python Bioload/BioLoad.py TOV_43_PCs.clstr Bioload/infofile.txt cdhit1.clstr cdhit2.clstr cdhit3.clstr`

**User input:**

When you run the program you will be asked:

- **Database IP:** the IP where the MySQL server is located (Just press enter to use the default values).
- **Database port:** the port where the MySQL server is located (Just press enter to use the default values).
- **Database user:** The user-name to log in to the MySQL server, this will be used to create a database and a table, so make sure it has the appropriate permissions.
- **Database password:** the password for the MySQL server user.
- **Delete and re-create previous databases? (y/n):** you need to put "y" on the first run, or after updates that require you to create the database from scratch.
- **Delete and re-create previous info tables? (y/n):** you need to put "y" on the first run, or after updates that require you to create the info table from scratch.
- **Delete and re-create previous CD-HIT database? (y/n):** you need to put "y" if you don't have the same CD-HIT input as the last time that you ran the program.

**Example files:**

* **VirS1:**(CD-HIT output) https://www.dropbox.com/s/ckbscd1k6tfvy9t/VirS1_novel.clstr?dl=1

* **VirS2:**(CD-HIT output) https://www.dropbox.com/s/bstd3qdecwmqcg0/VirS2_novel.clstr?dl=1

* **VirS3:**(CD-HIT output) https://www.dropbox.com/s/9mroxhcxern3633/VirS3_novel.clstr?dl=1 

* **TOV:**(Tara file) https://www.dropbox.com/s/ty6m9yv2rj8lafb/TOV43_PCs.clstr?dl=1

  The VirS1, VirS2, VirS3, Are outputs of the CD-HIT so you can use them with the line: `python bioload TOV_43_PCs.clstr infofile.txt VirS1_novel.clstr VirS2_novel.clstr VirS3_novel.clstr`

**References**

[Brum, Jennifer R., J. Cesar Ignacio-Espinoza, Simon Roux, Guilhem Doulcier, Silvia G. Acinas, Adriana Alberti, Samuel Chaffron et al. "Patterns and ecological drivers of ocean viral communities." *Science* 348, no. 6237 (2015): 1261498.](http://science.sciencemag.org/content/348/6237/1261498)

