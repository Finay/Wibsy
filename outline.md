# WIBSY
### Will I Be Seeing You?

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
    - userdb: id, name, profile, username?, password??
2. Friends
    - friendsdb: userid1, userid2
    - requestsdb: initiatoruserid, recieveruserid, date
3. Travel
    - traveldb: userid, destination, date, description
4. Sharing
    - User can add and see friend plans (only when authorized)
--- 

## Stage 2
3D UI
- Low poly aesthetic + map
- Flight animation?
- Timeline
- Multi in city??