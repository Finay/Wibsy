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
Home (Pre-login)
- Register / Login options
Home (Post-login)
- No scroll
- Central low poly globe with friend markers
- Timeline controller bar on bottom
- Friend list on left
    - Toggle show
    - Accept requests

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