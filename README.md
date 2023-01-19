# Simmer The Toads

Simmer The Toads aims to refine playlists of varying artists and genres to
gradually transition from various music styles to create a cohesive listening
experience.

[Link to Asana project](https://app.asana.com/0/1203117920538793/1203117920538793)

[Final Planning Documentation](https://docs.google.com/document/d/1mxL4wcjIboUZs82ka1uiGlvUL_izlJdRB-PtG3yicJk/edit?usp=sharing)

## Table of Contents

- [Simmer The Toads](#simmer-the-toads)
  - [Table of Contents](#table-of-contents)
- [Elevator Pitch](#elevator-pitch)
  - [Why do we want to do this?](#why-do-we-want-to-do-this)
  - [Why is it cool?](#why-is-it-cool)
  - [Why is it achievable?](#why-is-it-achievable)
  - [Possible Questions](#possible-questions)
    - [How do you plan on implementing / doing this?](#how-do-you-plan-on-implementing--doing-this)
    - [What kind of (relevant) Spotify APIs exist?](#what-kind-of-relevant-spotify-apis-exist)
    - [How is this different from the existing project "Boil The Frog"?](#how-is-this-different-from-the-existing-project-boil-the-frog)
    - [What's up with "Simmer the Toads?"](#whats-up-with-simmer-the-toads)
- [Developer Environment Setup](#developer-environment-setup)

# Elevator Pitch

## Why do we want to do this?

Consider this situation: you are stuck on a long road trip with many people you
don't know. Naturally, you all have differing music tastes, and so there is
little cohesion between all the different songs you may add. Simmer The Toads
aims to solve this problem (and many others!) by creating a collaborative
Spotify playlist platform, which not only allows yourself and friends to create
playlists but to seamlessly transition between music of one style to another.

## Why is it cool?

To many of us, music has become more than a daily part of our lives. We listen
to and explore new artists all the time. A collaborative playlist service where
we can come together to listen to the music that we already enjoy, but also
gently expand our tastes does not exist. Such a platform would aid in artist and
genre discovery and even help get you more acquainted with the music tastes of
your friends.

## Why is it achievable?

Spotify has an exceedingly open and diverse set of resources for developers. We
can take advantage of much of the existing music recommendation tool-set and
build a cohesive platform with tight integration with Spotify. There is a
project called "Boil The Frog" which already does something similar, but is
rather limited, as it recommends a singular path of songs from one artist to
another. We look to "Boil The Frog" as more of a proof of concept, which
demonstrates our goals are achievable.

## Possible Questions

### How do you plan on implementing / doing this?

- We plan on building a website (or some other equivalent platform) which allows
  invited members to add songs to a collaborative playlist. Then, utilizing the
  existing Spotify recommendations APIs, analyze each song within the playlist
  and identify distinct genres and styles. Essentially, group the songs into
  stylistic categories. We can search for songs matching these categories, and
  fill in large stylistic gaps with "transition" songs.

### What kind of (relevant) Spotify APIs exist?

- Playlist Interactions (Add, remove, update, etc.)
- Track audio features, analysis, and recommendations.
- Genre seeds for recommendation analytics.

### How is this different from the existing project "Boil The Frog"?

- Boil The Frog takes two artists and creates a playlist gradually transitioning
  from one to the other. While fundamentally similar, Simmer The Toads aims to
  reorder an existing playlist, while adding transition songs when necessary, to
  seamlessly shift between artists and (more importantly) musical styles. We
  also plan to add collaborative playlist creation features.

### What's up with "Simmer the Toads?"

- When you boil frogs, you don't put them in a hot pot initially - they'll
  just jump straight out. You slowly but surely turn up the heat! "Boil the
  Frogs" refers to slowly but surely changing the genre - so before you know
  it, you'll go from Taylor Swift to Five Finger Death punch. Simmer the Toads
  is our homage to Boil the Frogs, hence the synonymical name

# Developer Environment Setup

1.  Install [Python 3.8](https://www.python.org/downloads/) or later.

2.  Navigate to the root of this repository then create and activate a virtual
    environment.

        $ python3 -m venv env
        $ source env/bin/activate # mac/linux
        $ env/bin/activate.bat    # windows

3.  Install the project dependencies.

        $ pip install .

4.  Start the development web server.

        $ flask --debug --app SimmerTheToads run
