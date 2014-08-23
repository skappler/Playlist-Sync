Playlist-Sync
=============

A python tool to sync m3u playlists

Usage: m3u-sync.py path-to-dest path-to-music m3u-file [--update]

path-to-dest is the destination folder where the content will be copied to

path-to-music is the source folder where all songs of the playlist must be contained

m3u-file is the path to the m3u file to sync

If --update is passed, md5 sums will be calculated for all files and compared in order to see if some metadata has changed
