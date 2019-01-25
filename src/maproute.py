#!/usr/bin/env python

import sys
import sqlite3

class MapRoute:
    def __init__(self):
        self.locations_by_room_id = {}
        self.exits_by_id = {}
        self.exits_by_exit = {}

        self.return_alias = None

        self.db = self.database_connect()
        self.load_locations()
        self.load_exits()

    def database_connect(self):
        con = sqlite3.connect('src/quow.db')
        con.row_factory = sqlite3.Row
        return con

    def load_locations(self):
        cur = self.db.cursor()
        cur.execute("SELECT room_id, map_id, xpos, ypos, room_short, room_type FROM rooms")
        for row in cur.fetchall():
            self.locations_by_room_id[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
            self.exits_by_id[row['room_id']] = {}
            self.exits_by_exit[row['room_id']] = {}

    def load_exits(self):
        cur = self.db.cursor()
        cur.execute("SELECT room_id, connect_id, exit FROM room_exits")
        for row in cur.fetchall():
            if self.exits_by_id.get(row['room_id']) is not None and self.exits_by_id.get(row['connect_id']) is not None:
                self.exits_by_id[row['room_id']][row['connect_id']] = row['exit']
                self.exits_by_exit[row['room_id']][row['exit']]  = row['connect_id']

    def route_to_room(self, current_id, target_id, same_place):
        # If we can't match one of the room identifiers, back out
        if not current_id or not target_id or not self.locations_by_room_id.get(target_id) or not self.locations_by_room_id.get(current_id):
            return

        sDoPath, sFinalDestination, iResults = self.route_find(
            current_id, target_id, 
            self.locations_by_room_id[target_id][0],
            self.locations_by_room_id[target_id][1],
            self.locations_by_room_id[target_id][2],
            same_place
        )

        if sDoPath != "":
            sDoPath = "alias RuhsSpeedRun {}".format(sDoPath)
            if len(sDoPath) > 1700:
                pass
            else:
                self.return_alias = sDoPath

    def route_find(self, start_id, dest_id, dest_map, dest_x, dest_y, same_place=True):
        sDoRoom = [start_id]
        bEverDone = {start_id: True}
        sIDToRoomNum = {start_id: 1}
        iGotHereFrom = {}
        iNextRoom = 1
        iTotalRooms = 1
        sLinkedTo = []
        iSearchDepth = 0
        bDone = False
        iFinalRoom = 0
        iPreviousTotal = 0

        # "Infinite" loop
        while bDone == False:
            # Loop through all the rooms we have yet to do
            iPreviousTotal = iTotalRooms
            for iN in xrange(iNextRoom - 1, iPreviousTotal):
                # Loop through all exits from this room
                for sKey, sExitData in self.exits_by_id[sDoRoom[iN]].iteritems():
                    # Make sure we aren't looping back around on ourselves, and that we haven't already finished
                    if sKey != start_id and bEverDone.get(sKey) == None and iFinalRoom == 0:
                        iTotalRooms = iTotalRooms + 1
                        # Add THIS destination of THIS room to the "to-be-processed" list
                        sDoRoom.append(sKey)
                        # Flag this room so we never come here again
                        bEverDone[sKey] = True
                        # Record ID to room-num
                        sIDToRoomNum[sKey] = iTotalRooms
                        # Record back-tracking data
                        iGotHereFrom[iTotalRooms] = [sIDToRoomNum[sDoRoom[iN]], sExitData]
                        # See if we made it yet
                        if sDoRoom[iN] == dest_id:
                            bDone = True
                            iFinalRoom = iN
                        elif sKey == dest_id:
                            bDone = True
                            iFinalRoom = iTotalRooms
                        elif (same_place == True and self.locations_by_room_id[sDoRoom[iN]][0] == dest_map 
                              and self.locations_by_room_id[sDoRoom[iN]][1] == dest_x 
                              and self.locations_by_room_id[sDoRoom[iN]][2] == dest_y):
                            # Maybe we reached the co-ordinates instead - eg a house with multiple rooms in one pixels -- only stop here if we didn't START here
                            if (self.locations_by_room_id[start_id][0] != dest_map or 
                                    self.locations_by_room_id[start_id][1] != dest_x or 
                                    self.locations_by_room_id[start_id][2] != dest_y):
                                bDone = True
                                iFinalRoom = iN
                        # elif
                    # not back to beginning
                # loop through exit rooms
            # loop through "to-do"

            iNextRoom = iPreviousTotal + 1
            if iNextRoom > iTotalRooms:
                # Failed to find a route
                bDone = True
            iSearchDepth = iSearchDepth + 1
            if iSearchDepth > 500:
                # Failed, too deep
                bDone = True
                iFinalRoom = 0
                break
        # infinite loop end

        # Did we actually find a room?
        if iFinalRoom != 0:
            sPath = []
            bDone = False
            iCurRoom = iFinalRoom
            while bDone == False:
                sPath.append(iGotHereFrom[iCurRoom][1])
                iCurRoom = iGotHereFrom[iCurRoom][0]
                if iCurRoom == 1:
                    bDone = True
            sRealPath = ""
            for iN in xrange(len(sPath), 0, -1):
                if sRealPath != "":
                    sRealPath = "{};".format(sRealPath)
                sRealPath = "{}{}".format(sRealPath, sPath[iN-1])
            return sRealPath, sDoRoom[iFinalRoom-1], len(sPath)
        # Didn't find a route, return blanks
        return "", "", 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[error] No input provided.')
        sys.exit()

    current_room, target_room = sys.argv.pop(1), sys.argv.pop(1)

    router = MapRoute()
    router.route_to_room(current_room, target_room, True)
    # TODO: Can we determine samePlace? We need to compare the MapID of current_room and target_room when found?
    # d route between df6506b79c67080920fccbf27ce0d06cd392e01a and 03360211b315daf089d9ba329dd32417b9c7f54c.

    if router.return_alias:
        print(router.return_alias)
    else:
        print(0)
