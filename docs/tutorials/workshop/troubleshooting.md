---
title: "Troubleshooting"
description: "Problems met in the Depictio workshop, episode by episode, with their cause and fix."
---

# Troubleshooting

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-lifebuoy: **For learners**</span> <span class="ws-chip" markdown="span">:material-school-outline: **Instructors: see Instructor notes**</span>
</div>

Ask the docs assistant first: the chat button at the bottom right of these pages. If it does not answer, ask in the Zoom chat.

## :material-earth: Everywhere

| Symptom | Cause | Fix |
|---|---|---|
| Cannot sign in | Account not created, or a typo in the e-mail | Ask the instructor; use the Codespace meanwhile |
| **Dashboards** keeps sending you back to *Choose your own password* | The first sign-in asks for a new password | Set a new password: Dashboards then opens |
| A page stays blank | An old tab, or the browser blocks the server | Reload; try another browser |
| Fell behind | | Each episode has a ready-made result shared by the instructor: continue from it |

## :material-numeric-1-circle-outline: Episode 1 { #episode-1 .ws-ep1 }

| Symptom | Cause | Fix |
|---|---|---|
| Phyla does not change | Another filter was used | The **Habitat** filter of the left panel, on Community & Diversity |
| Six samples instead of three for *Groundwater* | Habitat takes several values: *Soil* is still selected | Remove *Soil*, keep only *Groundwater* |
| *General Statistics* finds nothing in the search | The table is named *General Stats* | Search for *General Stats* |
| No **Sampling sites** map, no **Environment (CTD)** tab | Your dashboard is the one built from the template, with 7 tabs | Skip challenges 1.5 and 1.6 |
| A filter is gone on another tab | It belongs to its tab's own section | Only a pinned section :material-pin: reaches every tab: **Sample filters** |
| No Box select | The toolbar shows on hover | Hover the figure: the toolbar is at its top right |
| The group was saved as *Group 1* | The name field is lower in the Analysis panel | Scroll the panel before **Save group** |
| No comment icon, or "not allowed" | The server does not let readers comment | Server setting, see [Instructor notes](facilitators.md#server-settings) |
| Groups are gone | Groups are kept per browser | Same browser, not a private window |

## :material-numeric-2-circle-outline: Episode 2 { #episode-2 .ws-ep2 }

| Symptom | Cause | Fix |
|---|---|---|
| No **Edit** button | You are on the shared dashboard | Open your copy from **Dashboards** |
| The figure is empty | Wrong data collection | **ancombc_results** |
| Code mode refuses the code | The server keeps figure code for admins | Use the form instead |
| **Next Step** greyed, no **Create component** | **Create component** is at the bottom of the left column | Scroll the left column |
| *Preview failed … timed out* | The server is busy reading other projects | Change any field to try again |

## :material-numeric-3-circle-outline: Episode 3 { #episode-3 .ws-ep3 }

| Symptom | Cause | Fix |
|---|---|---|
| "A project with this name already exists" | Names are unique on a server | Another name |
| The location is refused | Incomplete address | The full `s3://` address, without spaces |
| 22 collections instead of 23, no Differential Abundance tab | The group column was detected as `name` instead of `habitat`, so the ANCOM-BC results are not found | **Previous**, open **More pipeline settings**, set **Group column** to `habitat`, then **Next** |
| *phylogenetic_tree_canonical* failed, *NoSuchKey*; Phylogeny tab in error | The run location ends with `/`; the field's own placeholder ends with one | Create the project again with the location as given, with no final `/` |
| `sampling_sites.tsv` is not listed under **Upload**, or is not a table with map coordinates | The file was not dropped before **Next**, or it was edited | Download it again from the episode page and drop it in the left half of the first step |
| `metadata` is not in **Link your tables** | Depictio suggests at most 5 links per table | **Link it yourself**: `sampling_sites` to `metadata`, column `ID`; or **Add link** on the project page |
| One file URL: no **Add 1 table**, *has no table extension* | The ENA address ends without `.csv` or `.tsv` | Pick **Format**: **TSV**, and give a **Name**, `ena_runs` |
| One file URL is refused | The address starts with `http://`, which the server refuses unless its settings allow it | Use the `https://` address as given |
| The dashboard stays empty | Many projects are being read at once | Wait; **Activity** on the project page shows progress |

## :material-numeric-4-circle-outline: Episode 4 · Showcases { #episode-4 .ws-ep6 }

| Symptom | Cause | Fix |
|---|---|---|
| The showcases page does not load, or asks you to sign in | A stale tab, or you opened another server | Open [showcases.depictio.embl.org/dashboards](https://showcases.depictio.embl.org/dashboards){target=_blank} in a new tab: it is public, no sign-in |
| No showcase for your pipeline | Depictio has templates for 42 nf-core pipelines, and yours may not be one | Check the [list of templates](../../pipeline-templates/nf-core/index.md); otherwise open a pipeline from the poll |

## :material-alpha-a-circle-outline: Optional · Create a project from files { #optional-a .ws-ep4 }

| Symptom | Cause | Fix |
|---|---|---|
| No **Next** button in **New project** | The **Welcome** card, bottom right, covers it on a smaller screen | Close the Welcome card: **I'll explore on my own** |
| *1 file: 1 table* | Only one file was dropped | **Previous**, drop both files together |
| No **Add join** | Only the owner or an editor of a project can add a join, and the server must have the feature | Open the project you created in this episode; otherwise tell a helper |
| No Preview, *Pick both tables to preview the joined table* | A table is missing | **Name** `penguins`, `demographic_data` left, `physical_features` right, `individual_id` |
| No `joined_penguins` in the component's data list | The join was not created, or it has another name | The **Joins** list under **Cross-DC links**: its result table is `joined_<name>` |
| The figure cannot be coloured by `species` | The figure reads `physical_features`, which has no `species` | A figure of `joined_penguins` |
| **Edit** opens a title dialog | The **⋮ → Edit** menu edits the title and icon | Click the dashboard's title, then **Start editing** |
| The filter does not change a figure of `physical_features` | The filter and the figure read different tables, with no link between them | Build both on `joined_penguins` |
| No **Add group**, or the switches are greyed | Only the owner of a project can share it | Open the project you created in this episode |
| Your group is not in **Search groups** | The user groups were not created, or a typo | Tell a helper |
| Your group does not see your dashboard | The group was added to another project | **Permissions** of the right project: **Everyone with access** must list them |
