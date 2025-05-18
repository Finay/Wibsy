# WIBSY
### Will I Be Seeing You?


# Dev Plan
## Stage 1
Backend
- Users can login, add friends, view friends, add travel schedules
- Minimal UI
- DBs: Users, friends, requests, trips
- Security
    - Only view friends
    - Google signin
    - Cookies for autologin


1. Login system + User db
    - Start simple, more opt features later with db migration
    - Google stuff!
    - userdb: id, name, username?, password??
2. Friends
    - friendsdb: id, userid1, userid2, status
3. Travel
    - traveldb: userid, destination, date, description
4. Sharing
    - User can add and see friend plans (only when authorized)
---

## Stage 2
3D UI
- Low poly aesthetic + map
- Timeline
- Multi in city??

# Site Pages
## Home (Pre-login)
- Register / Login options
## Home (Post-login)
- No scroll
- Central low poly globe with friend markers
- Timeline controller bar on bottom
- Friend list on left
    - Toggle show
    - Accept requests
Globe Display Things
- Update travel entry to integrate location search
- Locations should match to lat/long coords
- Translate lat/long coords to polyglobe
- Need geographically accurate polyglobe
- Avatar geometry -> Clickable/toggle visibility
- Groups
- Return to home view
- Rotation controls
- Zoom to friend
- Distance controls???

Friend bar
- Controls for visibility
- scroll/search for users
- clean itinerary view?
- White bordered ui like among us?
-


### Avatar Logic
Loading
- Pull friends and their data from db
- Calculate locations with multiple people
- Convert coords into rotations (per unique coord)
    - Display multi for multi, avatars for individuals
Heiarchy
- World --> Everything that spins independent of the camera
    - Globe --> Low poly globe model
    -


- Menu on top right
    - Settings
    - Profile settings
    - Add travel
    - Add friend
    - Logout

# Later features
Profile & travel & friends editing
Photo related stuff??
Profile colors
Flight animation
moon?
Full public profile, no need to be friended


# Links
https://realpython.com/flask-google-login/
https://sketchfab.com/3d-models/low-poly-earth-5665f720773c41198116a3585dfae3af
https://developers.google.com/identity/gsi/web/tools/configurator
https://console.cloud.google.com/auth/clients?inv=1&invt=AbwSXw&project=wibsy-458604
https://myaccount.google.com/connections?pli=1


https://sketchfab.com/3d-models/low-poly-earth-c99483d5e2a94ca8b4f3579145584beb#download
