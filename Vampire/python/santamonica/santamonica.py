print "loading santa monica level script"
#function's comments indicate what map they are called on
import __main__

import fileutil
import random
import vamputil
import consoleutil

from __main__ import G

__main__.Level = __name__

Find = __main__.FindEntityByName
FindList = __main__.FindEntitiesByName

RandomLine = __main__.RandomLine

# added by wesp
def civilianDeath():
    pc = __main__.FindPlayer()
    if(pc.humanity >= 3):
        pc.HumanityAdd( -1 )

# added by RobinHood70
def spawnVandalBlood():
    pc = __main__.FindPlayer()
    if(pc.AmmoCount("item_g_bluebloodpack") == 0):
        pc.GiveItem("item_g_bluebloodpack")
    elif (pc.AmmoCount("item_g_bluebloodpack") >= 10):
        vandal = Find("Vandal")
        center = vandal.GetCenter()
        point = (center[0], center[1], center[2] + 20)
        blood = __main__.CreateEntityNoSpawn("item_g_bluebloodpack", point, (0,0,0) )
        blood.SetName("vandal_blood")
        sparklies = __main__.CreateEntityNoSpawn("inspection_node", point, (0,0,0) )
        sparklies.SetParent("vandal_blood")
        __main__.CallEntitySpawn(blood)
        __main__.CallEntitySpawn(sparklies)
    else:
        pc.GiveAmmo("item_g_bluebloodpack", 1)

#PAWNSHOP
def apartmentLeave():
    if(G.Story_State == 90):
        __main__.ChangeMap(2.5, "apartment1", "ApartmentTeleport2")
    else:
        __main__.ChangeMap(2.5, "apartment1", "ApartmentTeleport1")

#APARTMENT: called when carson's computer is hacked
def carsonComputerHacked():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Arthur Knox")
    if(state > 0 and state < 2):
        pc.SetQuest("Arthur Knox", 2)

#APARTMENT (AND ASYLUM): Called to see if the elysium load tip is done, changed by wesp
def finishElysiumTip():
    print "elysium tip done"
    if(G.Elysium_Tip == 1):
        G.Elysium_Tip = 2
        G.Story_State = G.Story_State_Save
    if (G.Carson_Rescued == 1):
        computer = Find("Carson_Computer")
        if computer: computer.Kill()
    if G.Patch_Plus == 1:
        moolah = Find("moolah")
        sparklies = Find("moolah_sparklies")
        if moolah: moolah.ScriptUnhide()
        if sparklies: sparklies.ScriptUnhide()
        money = Find("money")
        sparklies = Find("money_sparklies")
        if money: money.ScriptHide()
        if sparklies: sparklies.ScriptHide()

#APARTMENT: called when the player picks up the journal in Mercurio's
def journalPickup():
    if(G.Mercurio_Quest < 2):
        pc = __main__.FindPlayer()
        pc.SetQuest("Warehouse", 6)
        pc.SetQuest("Astrolite", 7)
        G.Mercurio_Quest = 2

#APARTMENT: determines which model Mercurio should use
def updateMercurioModel():
    npc = Find("Mercurio")
    if(G.Story_State >= 5 and G.Story_State < 15):
        if npc: npc.ScriptHide()
    if(G.Story_State >= 15 and G.Prince_Mercurio == 0):
        if npc:
            npc.ScriptUnhide()
            npc.SetModel("models/character/npc/unique/Santa_Monica/Mercurio/Mercurio.mdl")
            npc.SetDisposition("Neutral", 1)
        teleporter = Find("healthy_mercurio_spot")
        teleporter.Teleport()
        script = Find("mercurio_turn_around")
        script.StartSchedule()
    elif(G.Prince_Mercurio):
        npc.Kill()

#APARTMENT: called to see if Mercurio needs his new camera
def mercurioCamera():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Astrolite")
    if(G.Story_State > 5 or state == 5):
        pc = __main__.FindPlayer()
        pc.SetCamera("DialogDefault")

#APARTMENT: called when Mercurio is killed
def mercurioDeath():
    pc = __main__.FindPlayer()
    G.Mercurio_Dead = 1
    state = pc.GetQuestState("Astrolite")
    if(state == 5):
        pc.SetQuest("Astrolite", 6)
    world = Find("world")
    world.SetSafeArea(1)

#APARTMENT: called upon talking to Mercurio
def mercurioDialog():
    if(G.Mercurio_Attack == 1):
        world = Find("world")
        world.SetSafeArea(0)
        mercurio = Find("Mercurio")
        mercurio.SetRelationship("player D_HT 5")

#APARTMENT: called to see if Mercurio wants to fight
def mercurioFight():
    npc = Find("Mercurio")
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Astrolite")
    if(state == 5):
        if npc:
            npc.SetModel("models/character/npc/unique/Santa_Monica/Mercurio/Mercurio.mdl")
            npc.SetDisposition("Neutral", 1)
        teleporter = Find("healthy_mercurio_spot")
        teleporter.Teleport()
        script = Find("mercurio_turn_around")
        script.StartSchedule()
        trigger = Find("mercurio_angry_talk_trigger")
        trigger.Enable()
        journal = Find("mercurio_journal")
        journal.ScriptUnhide()
        sparklies = Find("journal_sparklies")
        sparklies.ScriptUnhide()
    if(__main__.IsDead("Mercurio")):
        npc.Kill()

#ASIAN VAMP ARENA: called when vamp is killed, changed by wesp
def asianVampDeath():
    __main__.FindPlayer().SetQuest("Knox Asian", 3)
    shu = Find("AsianVamp")
    center = shu.GetCenter()
    point = (center[0], center[1], center[2] + 20)
    blade = __main__.CreateEntityNoSpawn("item_w_chang_blade", point, (0,0,0) )
    blade.SetName("shinto")
    sparklies = __main__.CreateEntityNoSpawn("inspection_node", point, (0,0,0) )
    sparklies.SetParent("shinto")
    __main__.CallEntitySpawn(blade)
    __main__.CallEntitySpawn(sparklies)
    cross = __main__.CreateEntityNoSpawn("item_w_mac_10", point, (0,0,0) )
    cross.SetName("bow")
    sparklies1 = __main__.CreateEntityNoSpawn("inspection_node", point, (0,0,0) )
    sparklies1.SetParent("bow")
    __main__.CallEntitySpawn(cross)
    __main__.CallEntitySpawn(sparklies1)

#ASYLUM: unlocks the elevator if Cal says ok
def calDialog():
    button = Find("downstairsbttn")
    if (G.Cal_Permission == 1):
        button.Unlock()

#ASYLUM: opens the elevator only if the player has Cal's Permission
def checkElevatorPermission():
    button = Find("downstairsbttn")
    if (G.Cal_Permission == 1):
        button.Unlock()
    else:
        button.Lock()

#ASYLUM: determines if chunk is in the asylum, changed by wesp
def chunkDancing():
    chunk = Find("Chunk")
    if(chunk and G.Chunk_Dominated == 2 and G.Story_State < 10 and G.Chunk_Dead == 0 and not __main__.IsDead("Chunk")):
        chunk.ScriptUnhide()

#ASYLUM: called after talking to Danielle
def danielleDialog():
    if(G.Vandal_Quest == 3):
        danielle = Find("Danielle")
        danielle.UseInteresting(1)
        danielle.WillTalk(0)

#ASYLUM: plays the conversation between the Voermans the first time the PC uses the elevator
def elevatorConversation():
    npc = Find("Therese")
    #play conversation then opens doors after it's over
    if(G.Asylum_Visited == 0):
        __main__.ScheduleTask(55.0, "G.Asylum_Visited = 1")
        relay = Find("argument_relay")
        relay.Trigger()
    #just opens doors
    else:
        relay = Find("second_floor_relay")
        relay.Trigger()
        door = Find("bathroom_door")
        door.Unlock()
        door = Find("bedroom_door")
        door.Unlock()

#ASYLUM: determines whether or not Knox is present
def knoxPresence():
    IsDead = __main__.IsDead
    if (G.Mercurio_Quest >= 2 and not IsDead("Knox")):
        knox = Find("Knox")
        knox.ScriptUnhide()

#ASYLUM: called upon finishing dialogue with jeanette, changed by wesp
def jeanetteDialog():
    if(G.Jeanette_Boink == 1):
        relay = Find("jeanette_boink_relay")
        relay.Trigger()
        G.Jeanette_Boink = 2

#ASYLUM: places Jeanette downstairs in the Asylum and forces dialog
#if she has not yet met the player
def jeanetteDownstairs():
    npc = Find("Jeanette")
    interactions = npc.times_talked
    trigger = Find("bring_Jeanette_down")
    npc.UseInteresting(0)
    if (interactions == 0 and G.Therese_Quest < 2):
        npc.SetDisposition("Flirtatious", 1)
        trigger.Teleport()
        trigger = Find("Jeanette_dialog")
        trigger.Enable()
        trigger = Find("wait_for_elevator_relay")
        trigger.Enable()
    else:
        guy = Find("jeanette_flirt_partner")
        guy.UseInteresting(1)

#ASYLUM: gets rid of Jeanette when she "rides the elevator" up to the office
def jeanetteGoesUp():
    if (G.Cal_Permission != 1):
        npc = Find("Jeanette")
        npc.ScriptHide()

#ASYLUM: determines which version of Therese/Jeanette/Tourette to place
#in the office
def populateOffice():
    therese = Find("Therese")
    jeanette = Find("Jeanette")
    tourette = Find("Tourette")
    jeanette_pc = Find("jeanette_pc_blocker")
    therese_pc = Find("therese_pc_blocker")
    trigger = Find("Therese_mad_trigger")
    pc = __main__.FindPlayer()
    state_hotel = pc.GetQuestState("Hotel")
    state_slash = pc.GetQuestState("Slashterpiece")
    if (G.Therese_Quest < 2):
        if(G.Jeanette_Know == 1):
            jeanette.ScriptHide()
            tourette.ScriptHide()
            therese.ScriptUnhide()
        else:
            jeanette.ScriptUnhide()
            tourette.ScriptHide()
            therese.ScriptUnhide()
    elif (G.Therese_Quest >= 2 and G.Therese_Quest < 3 and G.Jeanette_Quest < 2 and G.Jeanette_Refuse < 1):
        jeanette.ScriptUnhide()
        jeanette_pc.ScriptUnhide()
        therese_pc.ScriptHide()
        jeanette.UseInteresting(1)
        tourette.ScriptHide()
        therese.ScriptHide()
    elif (G.Jeanette_Quest == 2 and G.Therese_Quest < 4):
        jeanette.ScriptHide()
        tourette.ScriptHide()
        therese.ScriptUnhide()
        jeanette_pc.ScriptHide()
        therese_pc.ScriptUnhide()
        trigger.Enable()
    elif(state_hotel > 3 and state_hotel < 6 and state_slash == 0):
        jeanette.ScriptHide()
        tourette.ScriptHide()
        therese.ScriptUnhide()
        jeanette_pc.ScriptHide()
        therese_pc.ScriptUnhide()
        trigger.Enable()
    elif (G.Jeanette_Refuse >= 1 and G.Jeanette_Fire < 3 and G.Therese_Quest < 3):
        jeanette.ScriptHide()
        tourette.ScriptHide()
        therese.ScriptHide()
        jeanette_pc.ScriptHide()
        therese_pc.ScriptHide()
    elif (G.Jeanette_Fire == 3 and G.Therese_Quest < 4):
        jeanette.ScriptHide()
        tourette.ScriptHide()
        therese.ScriptUnhide()
        jeanette_pc.ScriptHide()
        therese_pc.ScriptUnhide()
        trigger.Enable()
    elif (G.Therese_Quest == 4 and not G.Tourette_Wins and not G.Therese_Dead and not G.Jeanette_Dead):
        jeanette.ScriptHide()
        tourette.ScriptUnhide()
        jeanette_pc.ScriptUnhide()
        therese_pc.ScriptUnhide()
        trigger = Find("tourette_trigger")
        trigger.Enable()
        relay = Find("tourette_sequence_relay")
        relay.Trigger()
        therese.ScriptHide()
    elif(G.Tourette_Wins == 1 or G.Therese_Dead == 1 or G.Jeanette_Dead == 1):
        if(G.Story_State < 10):
            jeanette.ScriptHide()
            tourette.ScriptHide()
            therese.ScriptHide()
            jeanette_pc.ScriptHide()
            therese_pc.ScriptHide()
        elif (G.Tourette_Wins == 1):
            jeanette.ScriptHide()
            tourette.ScriptUnhide()
            therese.ScriptHide()
            jeanette_pc.ScriptUnhide()
            therese_pc.ScriptUnhide()
        elif (G.Jeanette_Dead == 1):
            jeanette.ScriptHide()
            tourette.ScriptHide()
            therese.ScriptUnhide()
            jeanette_pc.ScriptHide()
            therese_pc.ScriptUnhide()
        elif (G.Therese_Dead == 1):
            jeanette_pc.ScriptUnhide()
            therese_pc.ScriptHide()
            jeanette.ScriptUnhide()
            tourette.ScriptHide()
            therese.ScriptHide()
    else:
        print "Unaccounted for case:"
        print "  Not sure who (Therese/Tourette/Jeanette)"
        print "  should be in office"
    if(G.Vandal_Quest == 3):
        danielle = Find("Danielle")
        if danielle: danielle.Kill()

#ASYLUM: changes Tourette back to Therese if necessary
def touretteDialogueResults():
    if(G.Jeanette_Dead == 1):
        fade = Find("asylum_fade")
        fade.Fade()
        print "pre_switch"
        __main__.ScheduleTask(3.0, "__main__.FindEntityByName(\"Tourette\").SetModel(\"models/character/npc/unique/Santa_Monica/Therese/Therese.mdl\")")
        print "post_switch"
    elif(G.Tourette_Wins == 1):
        __main__.ChangeMap(2.5, "asylum1", "AsylumTeleport1")

#ASYLUM: makes the muzzle flash
def touretteMuzzleFlash():
    flash = Find("muzzle_flash")
    flash.TurnOn()

#BAILBONDS: called when Kilpatrick dies
def kilpatrickDeath():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Arthur Knox")
    if(state != 0 and state != 5):
        pc.SetQuest("Arthur Knox", 7)
    state = pc.GetQuestState("Bail Jumper")
    if(state != 0 and state != 3 and state != 4):
        pc.SetQuest("Bail Jumper", 5)

#BAILBONDS:  called when the player looks up rolf
def rolfViewed():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Lily")
    if(state == 7):
        pc.SetQuest("Lily", 9)
    #changed by dan_upright 04/12/04
    else:
        G.RolfTotenKnowledge = 1
    #changes end

#BAILBONDS: called when the player looks up virgil
def virgilViewed():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Knox Asian")
    if(state == 1 or state == 2 or state == 5):
        pc.SetQuest("Knox Asian", 9)
    #changed by dan_upright 04/12/04
    else:
        G.VirgilCrumbKnowledge = 1
    #changes end

#BASEMENT: called when carson dies
def carsonDeath():
    print "carson just died, do we care?"

#BASEMENT: called when gimble is killed
def gimbleDeath():
    __main__.FindPlayer().SetQuest("Arthur Knox", 3)
    G.Gimble_Dead = 1

#BEACHHOUSE: called when the player picks up astrolite
def astrolitePickup():
    pc = __main__.FindPlayer()
    if(G.Dennis_Alone == 0):
        pc.SetCriminalLevel(3)
    state = pc.GetQuestState("Astrolite")
    if(state == 4):
        pc.SetQuest("Astrolite", 5)
    else:
        pc.SetQuest("Astrolite", 2)

#BEACHHOUSE: called to check if the beachhouse should be hostile
def beachhouseStatus():
    if(G.Beachhouse_Hostile):
        dudes = __main__.FindEntitiesByClass("npc_VHumanCombatant")
        for dude in dudes:
            dude.SetRelationship("player D_HT 5")

#BEACHHOUSE: enforces the results of talking to brian at the beachouse
def brianDialogResults():
    print"brian"
    if(G.Brian_Permission or G.Brian_Wrong):
        script = Find("brian_move")
        print "move"
        if(script):
            script.BeginSequence()
        trigger = Find("pre_fence_anger")
        trigger.Disable()
        trigger = Find("post_fence_anger")
        trigger.Disable()
        if(G.Brian_Wrong):
            trigger = Find("ambush_trigger")
            trigger.Enable()
        #elif(G.Brian_Permission):
        #    script = Find("back_to_pizza")
        #    script.BeginSequence()
        #    script = Find("back_to_tv")
        #    script.BeginSequence()

#BEACHHOUSE: takes the appropriate action upon talking to Dennis
def dennisDialog():
    if(G.Dennis_Astrolite):
        astrolite = Find("astrolite")
        if astrolite: astrolite.ScriptHide()
        sparklies = Find("astrolite_sparklies")
        if sparklies: sparklies.ScriptHide()
    elif(G.Dennis_Alone):
        guard = Find("dennis_guard")
        if guard: guard.ScriptHide()

#BEACHHOUSE: restores story state after the load tip
def finishCombatTip():
    if(G.Combat_Tip == 1):
        G.Combat_Tip = 2
        G.Story_State = G.Story_State_Save

#BEACHHOUSE: sets up the NPCs at the beach house upon finding the player to be an enemy.
#No longer does anything.
def playerFoundAtBeachhouse():
    print ""
#    if(G.Beachhouse_Lights_Off):
        #do something
#        print "lights out"
#        relay = Find("spotted_lights_out_relay")
#        relay.Trigger()
#    else:
#        #do something else
#        script = Find("ambush_player_kitchen_surfer")
#        script.StartSchedule()
#        script = Find("ambush_player_dennis")
#        script.StartSchedule()
#        script = Find("ambush_player_dennis_surfer")
#        script.StartSchedule()

#BEACHHOUSE: makes the video game characters attack randomly
def randomFighterAttack(f):
    fighter = Find("fighter_%i" % (f))
    from random import Random
    from time import time
    R = Random( time() )
    attack = R.randint(1, 6)
    if(attack == 1):
        fighter.SetAnimation("claws_attack_low")
    elif(attack == 2):
        fighter.SetAnimation("fists_attack_shortright")
    elif(attack == 3):
        fighter.SetAnimation("claws_attack_medcombo")
    elif(attack == 4):
        fighter.SetAnimation("fists_dodge")
    elif(attack == 5):
        fighter.SetAnimation("katana_attack_sweepkick")
    elif(attack == 6):
        fighter.SetAnimation("katana_attack_flipkick")

#BLOODHUNT: called to ensure that no players get attacked by themselves
def bloodHuntClanCheck():
    brujah_model = "models/character/pc/male/brujah/armor0/brujah_Male_Armor_0.mdl"
    gangrel_model = "models/character/pc/male/gangrel/armor_2/Gangrel_Male_Armor_2.mdl"
    malkavian_model = "models/character/pc/male/malkavian/armor0/Malkavian_Male_Armor_0.mdl"
    nosferatu_model = "models/character/pc/male/nosferatu/armor0/Nosferatu.mdl"
    toreador_model = "models/character/pc/male/toreador/armor0/toreador_Male_Armor_0.mdl"
    ventrue_model = "models/character/pc/male/ventrue/armor1/ventrue_Male_Armor_1.mdl"
    pc = __main__.FindPlayer()
    clan = pc.clan
    obfuscate_users = FindList("obfuscate_*")
#    if(pc.IsMale()):
    if(1):
        #BRUJAH
        if(clan == 2):
            potence_users = FindList("potence_*")
            for potence_user in potence_users:
                potence_user.SetModel(nosferatu_model)
            celerity_users = FindList("celerity_*")
            for celerity_user in celerity_users:
                celerity_user.SetModel(toreador_model)
        #GANGREL
        elif(clan == 3):
            fortitude_users = FindList("fortitude_*")
            for fortitude_user in fortitude_users:
                fortitude_user.SetModel(ventrue_model)
            #NOTHING NEEDED FOR PROTEAN, THEY CAN BE BEASTFORM
        #MALKAVIAN
        elif(clan == 4):
            auspex_user = Find("auspex_1")
            if auspex_user: auspex_user.SetModel(toreador_model)
            fortitude_users = FindList("fortitude_*")
            for fortitude_user in fortitude_users:
                fortitude_user.SetModel(gangrel_model)
        #NOSFERATU
        elif(clan == 5):
            G.Bloodhunt_Obfuscate = 1
            for obfuscate_user in obfuscate_users:
                obfuscate_user.SetModel(malkavian_model)
            potence_users = FindList("potence_*")
            for potence_user in potence_users:
                potence_user.SetModel(brujah_model)
        #TOREADOR
        elif(clan == 6):
            presence_user = Find("presence_1")
            if presence_user: presence_user.SetModel(ventrue_model)
            celerity_users = FindList("celerity_*")
            for celerity_user in celerity_users:
                celerity_user.SetModel(brujah_model)
            potence_users = FindList("potence_*")
            for potence_user in potence_users:
                potence_user.SetModel(nosferatu_model)
            G.Bloodhunt_Obfuscate = 1
            for obfuscate_user in obfuscate_users:
                obfuscate_user.SetModel(malkavian_model)
        #TREMERE
        elif(clan == 7):
            #TREMERE NEED DO NOTHING
            potence_users = FindList("potence_*")
            for potence_user in potence_users:
                potence_user.SetModel(nosferatu_model)
            print "tremere"
        #VENTRUE
        elif(clan == 8):
            fortitude_users = FindList("fortitude_*")
            for fortitude_user in fortitude_users:
                fortitude_user.SetModel(gangrel_model)
    for obfuscate_user in obfuscate_users:
        obfuscate_user.ScriptHide()

#BLOODHUNT: called to see if the obfuscators should use potence
def obfuscatorsCheck():
    if(G.Bloodhunt_Obfuscate == 0):
        obfuscate_users = FindList("obfuscate_*")
        for obfuscate_user in obfuscate_users:
            obfuscate_user.SetScriptedDiscipline("potence 3")

#BLOODHUNT: called to see if Trip or Mercurio will still deal during the bloodhunt
def openShops():
    IsDead = __main__.IsDead
    if(not IsDead("Trip")):
        door = Find("trips_door")
        door.Unlock()
    if(not IsDead("Mercurio") and G.Mercurio_Attack == 0):
        door = Find("apartment_door_right")
        door.Unlock()
        door = Find("apartment_door_left")
        door.Unlock()
    #puts angry Ghouls on the map
    if(not IsDead("Knox") and G.Knox_Pissed > 0):
        knox = Find("Knox")
        if knox: knox.ScriptUnhide()
    if(not IsDead("Mercurio") and G.Mercurio_Attack == 1 and G.Prince_Mercurio == 0):
        mercurio = Find("Mercurio")
        if mercurio: mercurio.ScriptUnhide()

#BLOODHUNT: called by caine to transition to the taxi map
def toCaineTaxi():
    __main__.ChangeMap(2.5, "Caine_landmark", "CaineTeleport1")

#CAINE: called by caine in his cab to transition you to the appropriate ending location
def caineToFinale():
    pc = __main__.FindPlayer()
    # Changed By CompMod
    # clan = pc.clan
    clan = __main__.G._pcinfo["clan"]
    if(G.Caine_Business):
        #KUEI JIN
        if(G.Story_State == 100):
            if(not G.Ming_Ending):
                __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportTemple")
            else:
                if(clan == 5):
                    __main__.ChangeMap(2.5, "ventrue_nosferatu_entrance", "CaineTeleportVentrue1bNos")
                else:
                    __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportVentrue1b")
        #PRINCE
        elif(G.Story_State == 110):
            if(not G.Prince_Ending):
                #NOS
                if(clan == 5):
                    __main__.ChangeMap(2.5, "caine_nos_landmark", "CaineTeleportVentrue1Nos")
                else:
                    __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportVentrue1")
            else:
                __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportTemple")
        #ANARCHS
        elif(G.Story_State == 115):
            if(not G.Nines_Ending):
                __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportLuckystar")
            else:
                if(not G.Ming_Dead):
                    __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportTemple")
                else:
                    if(clan == 5):
                        __main__.ChangeMap(2.5, "ventrue_nosferatu_entrance", "CaineTeleportVentrue1bNos")
                    else:
                        __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportVentrue1b")
        #CAMARILLA
        elif(G.Story_State == 120):
            if(not G.Regent_Ending):
                __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportChantry")
            else:
                if(not G.Ming_Dead):
                    __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportTemple")
                else:
                    if(clan == 5):
                        __main__.ChangeMap(2.5, "ventrue_nosferatu_entrance", "CaineTeleportVentrue1bNos")
                    else:
                        __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportVentrue1b")
        #LONEWOLF
        elif(G.Story_State == 125):
            if(not G.Ming_Dead):
                __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportTemple")
            else:
                if(clan == 5):
                    __main__.ChangeMap(2.5, "ventrue_nosferatu_entrance", "CaineTeleportVentrue1bNos")
                else:
                    __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportVentrue1b")
    elif(G.Caine_Trip):
        relay = Find("to_trip_relay")
        relay.Trigger()
    elif(G.Caine_Mercurio):
        relay = Find("to_mercurio_relay")
        relay.Trigger()
    elif(G.Caine_Vandal):
        relay = Find("to_vandal_relay")
        relay.Trigger()
    elif(G.Caine_Haven):
        if(G.Regent_Family == 3):
            __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportChantry")
        elif(G.Prince_Skyline):
            __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportSkyline")
        elif(G.Gary_Haven):
            __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportSewer")
        else:
            __main__.ChangeMap(2.5, "caine_landmark", "CaineTeleportSMHaven")

#CLINIC: puts virgil's corpse and goods in the morgue if he's dead
def gimbleDead():
    if(G.Knox_Quest == 5):
        trunk = Find("morgue_trunk")
        trunk.AddEntityToContainer("gimble_ring")
        trunk.AddEntityToContainer("gimble_key")
        gimble = Find("gimble")
        gimble.ScriptUnhide()

#CLINIC: called when gimble's key is retrieved
def gimbleItemPickup():
    if(__main__.FindPlayer().HasItem("item_k_gimble_key")):
        __main__.FindPlayer().SetQuest("Knox Asian", 7)

#CLINIC: determines if the guard grants the player permission to be upstairs in the clinic
def guardDialog():
    if(G.Guard_Dominated or G.Guard_Open):
        if(G.Clinic_Upstairs_Safe == 0):
            G.Clinic_Upstairs_Safe = 1
            triggers = __main__.FindEntitiesByName("restricted_section")
            for trigger in triggers:
                trigger.Kill()
            trigger = Find("guard_warning")
            trigger.Kill()
            script = Find("guard_to_cs")
            script.Kill()
            script = Find("guard_to_prescriptions")
            script.Kill()
            trigger = Find("player_on_floor_two")
            trigger.Kill()
        if(G.Guard_Dominated == 1):
            G.Guard_Dominated = 2
            G.Guard_Open = 2
            spawnCSKey()
        if(G.Guard_CS == 1):
            G.Guard_CS = 2
            G.Guard_Open = 2
            teleport = Find("cs_teleport")
            teleport.Teleport()
            teleport = Find("player_teleport_cs")
            teleport.Enable()
            teleport.Kill()
            camera = Find("guard_follow_camera")
            camera.StartShot()
            script = Find("guard_to_cs_door")
            script.BeginSequence()
            __main__.ScheduleTask(1.0, "__main__.FindEntityByName(\"player_cs_relay\").Trigger()")
        if(G.Guard_Open == 1):
            G.Guard_Open = 2
            teleport = Find("cis_teleport")
            teleport.Teleport()
            teleport = Find("player_teleport_cis")
            teleport.Enable()
            teleport.Kill()
            camera = Find("guard_follow_camera")
            camera.StartShot()
            script = Find("guard_to_cis_door")
            script.BeginSequence()
            __main__.ScheduleTask(1.0, "__main__.FindEntityByName(\"player_cis_relay\").Trigger()")
    elif(G.Guard_Warning >= 3):
        __main__.ScheduleTask(5.0, "__main__.FindEntityByName(\"clinic_guard\").SetRelationship(\"player D_HT 5\")")

#CLINIC: checks to see if Heather should be present in the Clinic, changed by wesp, RobinHood70
def heatherCheck():
    npc = Find("Heather")
    if npc:
        if(G.Heather_Drank == 1 or G.Story_State >=10):
            npc.Kill()
        else:
            npc.ScriptUnhide()
    if __main__.IsDead("Malcolm"):
        malcolm = Find("Malcolm")
        if malcolm: malcolm.Kill()
    if __main__.IsDead("Nurse"):
        nurse = Find("Nurse")
        if nurse: nurse.Kill()
    if __main__.IsDead("waiting_patient1") or __main__.IsDead("waiting_patient2") or __main__.IsDead("waiting_patient3") or __main__.IsDead("waiting_patient4") or __main__.IsDead("Nurse"):
        p1 = Find("waiting_patient1")
        p2 = Find("waiting_patient2")
        p3 = Find("waiting_patient3")
        p4 = Find("waiting_patient4")
        if p1: p1.Kill()
        if p2: p2.Kill()
        if p3: p3.Kill()
        if p4: p4.Kill()

#CLINIC: determines the results of a dialog with heather
def heatherDialog():
    if(G.Nurse_Warn == 3):
        guard = Find("first_floor_guard")
        guard.Spawn()
        guard = Find("clinic_guard")
        if guard: guard.SetRelationship("player D_HT 5")
        relay = Find("nurse_trigger_killer")
        relay.Trigger()
    if(G.Heather_Steve == 1):
        relay = Find("heather_ghoul_relay")
        relay.Trigger()

#CLINIC: checks to see if the keycard for upstairs can be deleted
def keycardCheck():
    G.Clinic_Keycard_Used = G.Clinic_Keycard_Used + 1
    if(G.Clinic_Keycard_Used == 2):
        __main__.FindPlayer().RemoveItem("item_k_clinic_cs_key")

#CLINIC: Determines if Lily has been killed yet or not, changed by wesp
def lilyCheck():
    if(G.Story_State > 35):
        lily = Find("Lily")
        if lily: lily.Kill()
    if G.Patch_Plus == 1:
        book_comp = Find("book_comp")
        book_compnode = Find("book_compnode")
        if book_comp: book_comp.ScriptUnhide()
        if book_compnode: book_compnode.ScriptUnhide()

#CLINIC: determines the results of dialog with Lily
def lilyDialog():
    if(G.Lily_Release and not G.Lily_Free):
        relay = Find("lily_relay")
        relay.Trigger()
    if(G.Lily_Free):
        sequence = Find("lily_leave")
        sequence.BeginSequence()
        lily = Find("Lily")
        lily.WillTalk(0)

#CLINIC: called when Lily is killed
def lilyKilled():
    __main__.FindPlayer().SetQuest("Lily", 4)

#CLINIC: called after lily's scene is done to switch out her model
def lilyScene():
    print "lily"
    lily = Find("Lily")
    lily.SetModel("models/character/npc/unique/Santa_Monica/Lily/Lily.mdl")
    __main__.ScheduleTask(0.1, "__main__.FindEntityByName(\"Lily\").SetDisposition(\"Neutral\", 1)")

#CLINIC: updates the player's journal upon picking up morphine
def morphinePickup():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Morphine")
    if(state == 1):
        pc.SetQuest("Morphine", 2)

#CLINIC: notes any results of talking to the nurse
def nurseDialog():
    if(G.Nurse_Force == 1):
        G.Nurse_Warn = G.Nurse_Warn + 1
        G.Nurse_Force = 0
    if(G.Nurse_Warn == 3):
        guard = Find("first_floor_guard")
        guard.Spawn()
        __main__.FindPlayer().SetCriminalLevel(2)
        guard = Find("clinic_guard")
        if guard: guard.SetRelationship("player D_HT 5")
        relay = Find("nurse_trigger_killer")
        relay.Trigger()
    if(G.Nurse_Flag or G.Nurse_Persuade):
        triggers = __main__.FindEntitiesByName("nurse_talk_trigger")
        for trigger in triggers:
            trigger.Kill()
        nurse = Find("Nurse")
        if nurse: nurse.WillTalk(0)

#CLINIC: puts Phil in the clinic at the appropriate time
def philCheck():
    if(G.E_Quest == 2):
        phil = Find("Phil")
        phil.ScriptUnhide()
        keypad = Find("fake_keypad")
        keypad.ScriptHide()
        keypad = Find("lily_keypad")
        keypad.ScriptUnhide()
    if(G.E_Quest == 3):
        lily = Find("Lily")
        if lily: lily.ScriptHide()

#CLINIC: phil drops a note when this is called
def philDropNote():
    phil = Find("phil")
    note = Find("phil_note")
    note.ScriptUnhide()
    origin = phil.GetOrigin()
    point = (origin[0], origin[1], origin[2])
    note.SetOrigin(point)

#CLINIC: spawns in the CS key if the guard dies, changed by wesp
def spawnCSKey():
    if(G.CS_Key == 0):
        G.CS_Key = 1
        guard = Find("clinic_guard")
        center = guard.GetCenter()
        point = (center[0], center[1], center[2])
        key = __main__.CreateEntityNoSpawn("item_k_clinic_cs_key", point, (0,0,0) )
        key.SetName("clinic_guard_key")
        __main__.CallEntitySpawn(key)
        sparklies = __main__.CreateEntityNoSpawn("inspection_node", point, (0, 0, 0))
        sparklies.SetParent("clinic_guard_key")
        __main__.CallEntitySpawn(sparklies)
        if (G.Guard_Warning < 3 and G.Self_Defense == 0):
            pc = __main__.FindPlayer()
            if(pc.humanity >= 3):
                pc.HumanityAdd( -1 )

#CLINIC: checks to see if the stairs key can be deleted
def stairsKeyCheck():
    G.Clinic_Stairs_Open = G.Clinic_Stairs_Open + 1
    if(G.Clinic_Stairs_Open == 2):
        __main__.FindPlayer().RemoveItem("item_k_clinic_stairs_key")

#CLINIC: updates the user's journal for drug stealing quest
def updateDrugQuest():
    __main__.FindPlayer().SetQuest("Trip Drugs", 2)

#CLINIC: Opens the door when the player gets vandal's position
def vandalDialog():
    if(G.Vandal_Permission):
        door = Find("employee_entrance")
        door.Unlock()

#CLINIC: called when Vandal dies
def vandalDeath():
    pc = __main__.FindPlayer()
    status = pc.GetQuestState("Danielle")
    if(status == 1):
        pc.SetQuest("Danielle", 3)

#CLINIC: Spawns in the werewolf blood if the player is on the quest
def werewolfBloodClinicEnter():
    if ( G.Werewolf_Quest == 1 ):
        garou_blood = Find("garou_blood")
        garou_blood.ScriptUnhide()
        left_door = Find("left_door")
        left_door.Lock()
        hack_door = Find("hack_door")
        hack_door.Lock()
        #doorknob = Find("cs_doorknob")
        #doorknob.Lock()

#CLINIC: called when the player grabs the garou blood
def werewolfBloodPickup():
    __main__.FindPlayer().SetQuest("Werewolf blood", 2)

#CLINIC: Updates flag if the player leaves the clinic with the werewolf blood
def werewolfBloodClinicExit():
    pc = __main__.FindPlayer()
    if ( pc.HasItem("item_g_werewolf_bloodpack" ) ):
        G.Werewolf_Quest = 3

#DINER: used in diner to determine if thugs should be present for attack, changed by wesp
def dinerAttack():
    doris = Find("Doris")
    script = Find("Doris_cower")
    sound = Find("RegisterDoris")
    if(G.Therese_Quest == 3):
        if(doris):
            doris.ScriptHide()
        if(script):
            script.ScriptHide()
        if(sound):
            sound.ScriptHide()
        trigger = Find("trigger_attack")
        trigger.Enable()
        relay = Find("spawner_relay")
        relay.Trigger()
        #world = Find("world")
        #world.SetSafeArea(0)
        patron = Find("diner_patron_male")
        if(patron):
            patron.ScriptHide()
        patron = Find("diner_patron_female")
        if(patron):
            patron.ScriptHide()
    else:
        if(doris):
            doris.ScriptUnhide()
        if(script):
            script.ScriptUnhide()
        if(sound):
            sound.ScriptUnhide()
        world = Find("world")
        world.SetCopGrace(0.0)
        patron = Find("diner_patron_male")
        if(patron):
            patron.ScriptUnhide()
        patron = Find("diner_patron_female")
        if(patron):
            patron.ScriptUnhide()
        trigger = Find("post_robbery_cop_call")
        if(trigger):
            trigger.ScriptHide()
    siren = Find("Siren Loop")
    if(siren):
        siren.StopSound()

#DINER: handles results of Doris' dialog
def dorisDialog():
    if(G.Doris_Scare > 0 and G.Doris_Scare <= 3):
        script = Find("Doris_Faint")
        script.BeginSequence()
    elif(G.Doris_Scare > 3):
        #print "kill"
        npc = Find("Doris")
        npc.TakeDamage(100)
#    elif(G.Doris_Purse == 1 and G.Lily_Purse == 0):
#        script = Find("doris_give_purse")
#        script.BeginSequence()

#DINER: determines if the serial killer is in the diner, changed by wesp
def killerInDiner():
    npc = Find("Killer")
    if(npc):
        if(G.Therese_Quest < 3 and G.Story_State < 4):
            npc.ScriptUnhide()
        else:
            npc.Kill()
    doris = Find("Doris")
    cook = Find("cook")
    male = Find("diner_patron_male")
    female = Find("diner_patron_female")
    if __main__.IsDead("Doris") or __main__.IsDead("cook"):
        if doris: doris.Kill()
        if cook: cook.Kill()
        if male: male.Kill()
        if female: female.Kill()
    if __main__.IsDead("diner_patron_male"):
        if male: male.Kill()
    if __main__.IsDead("diner_patron_female"):
        if female: female.Kill()

#DINER: called if you angrify the killer in the Diner
def killerInDinerAngry():
        killer = Find("Killer")
        fade = Find("Transform_fade")
        fade.Fade()
        killer.SetModel("models/character/monster/Animalism_Beastform/Animalism_Beastform.mdl")

#DINER: puts lilly's goods in the diner if they should be there # updated by Dheu
# Purses OnUse handler calls playerGotPurse
def lillyStuff():
    pc = __main__.FindPlayer()
    # Changed By CompMod
    possibility1 = (G.E_Quest == 1 and (5 == __main__.G._pcinfo["clan"] or __main__.IsDead("Doris")))
    possibility2 = pc.HasItem("item_p_occult_hacking")
    if possibility1 or possibility2:
        sparklies = Find("lilly_purse_sparklies")
        if sparklies: sparklies.ScriptUnhide()
        purse = Find("lilly_purse")
        if purse: purse.ScriptUnhide()

#DINER: gives the nosferatu player lilly's items from the diner
def playerGotPurse():
    #CompMod 1.3 Patch Edit
    G.Got_Lily_purse=1
    handleLilyQuestState()

# Called from Diner, but also Called From E dialog if player does
# things way out of order. IE: Get Spell Book, Get Purse, Summon Boo
# and THEN begin Lily Quest. This is called by the second question
# to E about where to start (implying he gives you these things).
def handleLilyQuestState():
    if G.E_Quest == 1 and G.Got_Lily_purse == 1 and G.Got_Lily_stuff == 0:
        # A little confusing but the intent is: if you talk to E a second
        # time after already getting the purse, we go ahead and give the
        # player the stuff if Doris is dead. But if she is not dead, we
        # want to player to have to talk to her. G.Doris_Purse is set to
        # 1 when you talk to her about lily and then playerGotPurse is
        # called.
        if G.Doris_Purse == 1 or __main__.IsDead("Doris") or 5 == __main__.G._pcinfo["clan"]:
            G.Got_Lily_stuff=1
            pc = __main__.FindPlayer()
            __main__.GiveItem(pc, "item_g_lilly_photo")
            __main__.GiveItem(pc, "item_g_bailbond_receipt")
            __main__.GiveItem(pc, "item_k_lilly_key")
            state = pc.GetQuestState("Lily")
            #changed by dan_upright 04/12/04
            if (G.RolfTotenKnowledge == 1 and state != 10):
                pc.SetQuest("Lily", 11)
            elif (state != 10):
                pc.SetQuest("Lily", 7)
            #changes end

#DINER: updates Quest status and makes the phone ring once attackers are subdued in the diner
def thugsAllDead():
    G.Therese_Quest = 4
    pc = __main__.FindPlayer()
    pc.SetQuest("Diner", 2)
    world = Find("world")
    world.SetSafeArea(1)
   # world.SetCopGrace(120.0)
    phone_ring = Find("phone_ring")
    phone_ring.PlaySound()
    phone = Find("SMphone")
    phone.WillTalk(1)
    controller = Find("controller")
    controller.ClearDialogCombatTimers()
    #this next part is temporary until the phone works
    #if(G.Jeanette_Seduce < 8):
    #   pc.SetQuest("Tourette", 2)
    #else:
    #    pc.SetQuest("Tourette", 1)

#EMBRACE: Assigns a player model to the player_understudy
def castUnderstudy():
    understudy = Find("player_understudy")
    pc = __main__.FindPlayer()
    clan = pc.clan
    player_model = pc.GetModelName()
    #NOS
    if(clan == 5):
        if(pc.IsMale()):
            understudy.SetModel("models/character/pc/male/brujah/armor0/brujah_Male_Armor_0.mdl")
        else:
            understudy.SetModel("models/character/pc/female/brujah/armor3/brujah_female_armor_3.mdl")
    else:
        understudy.SetModel(player_model)

#EMBRACE: transforms the understudy into a hideous creature if the player has chosen Nosferatu
def nosferatuTransform():
    understudy = Find("player_understudy")
    pc = __main__.FindPlayer()
    clan = pc.clan
    if(clan == 5):
        if(pc.IsMale()):
            understudy.SetModel("models/character/pc/male/nosferatu/armor0/Nosferatu.mdl")
        else:
            understudy.SetModel("models/character/pc/female/nosferatu/armor0/nosferatu_Female_Armor_0.mdl")

#HAVEN: sets quest state at start of the game
def beginningTheGame():
    #G.Haven_Bum gets set the first time the player goes out of his haven
    state = __main__.FindPlayer().GetQuestState("Mercurio")

    if(state < 1 ):
        __main__.FindPlayer().SetQuest("Mercurio", 1)
    if(G.Story_State <  0):
        G.Story_State = -1
#    if(0 == G.Story_State and vamputil.OnEnterMap("sm_oceanhouse_1")):


#HAVEN: called to see if the player should go straight to the taxi
def havenTaxiCheck():
    print "taxi check"
    if(G.Story_State >= 100):
        __main__.ChangeMap(2.5, "caine_landmark", "smhaven_caine")

#HAVEN: called to remove the invite when the player has got to the Regent, changed by wesp
def inviteGone():
    if(G.Regent_Introduced == 1):
        invite = Find("regent_invite")
        if invite: invite.Kill()
    if(G.Mercurio_Know == 1):
        note = Find("mercurios_note")
        if note: note.Kill()

#HAVEN: Jack visits the player after the observatory, changed by wesp
def jackVisit():
    if(G.Story_State == 90):
        jack = Find("Jack")
        jack.ScriptUnhide()
        relay = Find("bloodhunt_on_relay")
        relay.Trigger()
        world = Find("world")
        world.SetSafeArea(2)
    if(G.Story_State > 90):
        relay = Find("bloodhunt_off_relay")
        relay.Trigger()

#HAVEN: places the bribe from Malcolm in the player's haven, changed by wesp
def malcolmBribed():
    player_mail = Find("Mailbox_haven")
    if(player_mail and not __main__.IsDead("Malcolm")):
        if(G.Malcolm_Affair == 4):
            player_mail.AddEntityToContainer("small_bribe")
            G.Malcolm_Affair = 6
        elif(G.Malcolm_Affair == 5):
            player_mail.AddEntityToContainer("big_bribe")
            G.Malcolm_Affair = 6

#HAVEN: Locks the Santa Monica haven stuff when the PC acquires a new haven, changed by wesp
def lockHaven():
    if(G.Prince_Skyline or G.Gary_Haven or G.Regent_Family == 3):
        mailbox = Find("Mailbox_haven")
        if(mailbox):
            mailbox.SetName("Locked_mailbox_haven")
        #mailbox.ScriptHide()
        #mailbox = Find("locked_haven_box")
        #mailbox.ScriptUnhide()
        laptop = Find("haven_pc")
        laptop.ScriptHide()
        relay = Find("haven_emptier")
        relay.Trigger()
        if(G.Gary_Voerman):
            poster = Find("poster_jeanette")
            poster.ScriptHide()
        if(G.Velvet_Poster):
            poster = Find("poster_vv")
            poster.ScriptHide()
        if(G.Gary_Photochop):
            poster = Find("poster_ming")
            poster.ScriptHide()
        if(G.Gary_Damsel):
            poster = Find("poster_damsel")
            poster.ScriptHide()
        if(G.Gary_Tawni):
            poster = Find("poster_tawni")
            poster.ScriptHide()

#HAVEN: Called the first time the player reads the paper in the Haven
def murderPaperRead():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Serial")
    if(state == 0):
        pc.SetQuest("Serial", 1)

#HAVEN:  Place's murietta's key in the hallway
def muriettaGone():
    if (G.Arthur_Muddy == 2 ):
        machine = Find("answering_machine_button")
        if machine: machine.ScriptUnhide()
        key = Find("murietta_key")
        if key: key.ScriptUnhide()
        sparklies = Find("murietta_key_sparklies")
        if sparklies: sparklies.ScriptUnhide()
        sparklies = Find("answering_machine_sparklies")
        if sparklies: sparklies.ScriptUnhide()

#HAVEN: called when the player reads the regent's invite
def regentInvite():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Strauss")
    if(state == 0):
        pc.SetQuest("Strauss", 1)
        G.Regent_Invitation = 1

#HAVEN: Called to place the appropriate type of bloodpacks in the player's new haven.
def stockTheFridge():
    fridge = Find("haven_refrigerator")
    bloodpacks = 3
    while(bloodpacks > 0):
        if(__main__.IsClan(__main__.FindPlayer(), "Ventrue")):
            fridge.SpawnItemInContainer("item_g_bluebloodpack")
        else:
            fridge.SpawnItemInContainer("item_g_bloodpack")
        bloodpacks = bloodpacks - 1

#HAVEN: updates the user's journal for the bail jumper quest
def updateBailJumperQuest():
    G.Muddy_Message = 1
    G.SK_Downtown = 1
    __main__.FindPlayer().SetQuest("Bail Jumper", 2)

#JUNKYARD: called when Killer dies
def killerDeath():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Serial")
    if(state != 9):
        pc.ChangeMasqueradeLevel(-1)
        pc.SetQuest("Serial", 8)
    relay = Find("player_leave_relay")
    relay.Trigger()

#JUNKYARD:determines the killer's actions after confronting him
def killerHostileCheck():
    if(G.Killer_Hostile):
        killer = Find("Killer")
        fade = Find("Transform_fade")
        fade.Fade()
        killer.SetModel("models/character/monster/Animalism_Beastform/Animalism_Beastform.mdl")
        script = Find("killer_attack")
        G.Killer_Attacks = 1
        script.BeginSequence()
    else:
        relay = Find("player_leave_relay")
        relay.Trigger()

#JUNKYARD: transforms the killer
def killerTransform():
    killer = Find("Killer")
    killer.SetModel("models/character/monster/Animalism_Beastform/Animalism_Beastform.mdl")

#OCEANHOUSE: Fireaxe, added by wesp
def axeState():
    if G.Patch_Plus == 1:
        axe = Find("axe")
        axenode = Find("axenode")
        if axe: axe.ScriptUnhide()
        if axenode: axenode.ScriptUnhide()
        trunk = Find("Occult_Container")
        trunk.SpawnItemInContainer("item_p_research_lg_dodge")
    else:
        trunk = Find("Occult_Container")
        trunk.SpawnItemInContainer("item_p_occult_dodge")

#OCEANHOUSE: updates the player's quest book
def spirtQuestAssign():
    __main__.FindPlayer().SetQuest("Release the Spirit", 1)

#OCEANHOUSE: updates anything that happens when the map is completed.
def oceanhouseQuestComplete():
    __main__.FindPlayer().SetQuest("Hotel",2)
    G.Therese_Quest = 2

#OCEANHOUSE: updates the player's quest book
def spirtQuestComplete():
    __main__.FindPlayer().SetQuest("Release the Spirit", 3)

#PAWNSHOP
def pawnshopLeave():
    if(G.Story_State == 90):
        __main__.ChangeMap(2.5, "pawnshop1", "PawnshopTeleport2")
    else:
        __main__.ChangeMap(2.5, "pawnshop1", "PawnshopTeleport1")

#PIER: determines whether the player can access the beachhouse or not
def beachHouseOpen():
    gate = Find("beachhousegate")
    if(G.Mercurio_Quest == 1):
        gate.Unlock()
    elif(G.Mercurio_Quest > 1):
        gate.Lock()

#PIER: determines the state of Mercurio/Beachhouse guys on the beach
def beachVisitors():
    mercurio = Find("Mercurio")
    dennis = Find("Dennis")
    brian = Find("Brian")
    carl = Find("Carl")
    mike = Find("Mike")
    IsDead = __main__.IsDead
    state = __main__.FindPlayer().GetQuestState("Dane")
    if(state == 1 or state == 2):
        #Mercurio on beach
        if(state == 1 and G.Prince_Mercurio == 0  and not IsDead("Mercurio") and mercurio):
            mercurio.ScriptUnhide()
        #Mercurio gone
        elif(state == 2 and mercurio):
            mercurio.ScriptHide()
        #thugs maybe
        if((IsDead("Mercurio") or G.Prince_Mercurio) and G.Beach_Dead == 0 and state == 2):
            if(G.Dennis_Alone and not IsDead("Dennis") and dennis and carl and mike and brian):
                hideThinBloods()
                dennis.ScriptUnhide()
                carl.ScriptUnhide()
                if(IsDead("Brian")):
                    mike.ScriptUnhide()
                else:
                    brian.ScriptUnhide()
            if((IsDead("Brian") or IsDead("Dennis")) and not (IsDead("Brian") and IsDead("Dennis"))):
                hideThinBloods()
                if(carl and mike):
                    carl.ScriptUnhide()
                    mike.ScriptUnhide()
                if(IsDead("Brian") and dennis):
                    dennis.ScriptUnhide()
                elif(brian):
                    brian.ScriptUnhide()
            if(G.Dennis_Owe == 1 and not (IsDead("Brian") and IsDead("Dennis"))):
                hideThinBloods()
                if(mike):
                    mike.ScriptUnhide()
                if(IsDead("Brian")and dennis and carl):
                   dennis.ScriptUnhide()
                   carl.ScriptUnhide()
                elif(IsDead("Dennis") and brian and carl):
                   brian.ScriptUnhide()
                   carl.ScriptUnhide()
                elif(dennis and brian):
                    dennis.ScriptUnhide()
                    brian.ScriptUnhide()
    if(state > 2):
        unhideThinBloods()

#PIER: copper leaves the beach, changed by wesp
def copperDialog():
    if(G.Copper_Slayer):
        script = Find("copper_leaves")
        script.BeginSequence()
    if(G.Copper_Uni == 2 and G.Patch_Plus == 1):
        script = Find("copper_leaves")
        script.BeginSequence()

#PIER: hides the thinbloods during the thug ambush
def hideThinBloods():
    G.Thin_Bloods_Hidden = 1
    thinblood = Find("E")
    if(thinblood):
        thinblood.ScriptHide()
    thinblood = Find("Rosa")
    if(thinblood):
        thinblood.ScriptHide()
    thinblood = Find("Copper")
    if(thinblood):
        thinblood.ScriptHide()
    thinblood = Find("Julius")
    if(thinblood):
        thinblood.ScriptHide()
    thinblood = Find("Lily")
    if(thinblood):
        thinblood.ScriptHide()

#PIER: unhides the thinbloods after the thug ambush
def unhideThinBloods():
    if(G.Beach_Thugs_Dead == 3):
        G.Thin_Bloods_Hidden = 0
        thinblood = Find("E")
        if(thinblood):
            thinblood.ScriptUnhide()
        thinblood = Find("Rosa")
        if(thinblood):
            thinblood.ScriptUnhide()
        thinblood = Find("Copper")
        if(thinblood):
            thinblood.ScriptUnhide()
        thinblood = Find("Julius")
        if(thinblood):
            thinblood.ScriptUnhide()
        if(G.E_Quest > 2 and not __main__.IsDead("E")):
            # Added for companion mod
            if G.Lily_CompFeed == 0:
                thinblood = Find("Lily")
                if(thinblood):
                    thinblood.ScriptUnhide()

#PIER: gets the Combat load tip up on screen
def initCombatLoadTip():
    if(G.Combat_Tip == 0):
        G.Combat_Tip = 1
        G.Story_State_Save = G.Story_State
        G.Story_State = 3

#PIER: sends e to the ocean's edge if player is on the lilly quest
def eAtOceanEdge():
    if(G.Story_State < 35):
        e = Find("E")
        if(e):
            if(G.E_Quest > 0 and G.E_Quest < 3):
                e.UseInteresting(1)
            else:
                e.UseInteresting(0)

#PIER: called when e dies
def eDeath():
    #add quest stuff here when Leon tells you to
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Lily")
    if(state != 0 and state != 4 and state != 8):
        pc.SetQuest("Lily", 10)

#PIER: determines results of talking to Julius
def juliusDialog():
    if(G.Julius_Release):
        sequence = Find("julius_release_sequence")
        sequence.BeginSequence()
        julius = Find("Julius")
        julius.WillTalk(0)
    elif(G.Julius_Cringe):
        julius = Find("Julius")
        julius.SetRelationship("player D_FR 5")

#PIER: puts Lilly on the beach if she's been rescued
def lillyBack():
    if(G.E_Quest > 2 and not __main__.IsDead("E") and not G.Thin_Bloods_Hidden):
        #Added for companion mod
        if G.Lily_CompFeed == 0:
            lily = Find("Lily")
            if(lily):
                lily.ScriptUnhide()

#PIER: used in the pier to determine if the murder is still present
def murderCleanedUp():
    if(G.Story_State >= 10 and not G.Pier_Scene_Gone):
        G.Pier_Scene_Gone = 1
        blood = __main__.FindEntitiesByName("victimblooda")
        for b in blood:
            b.Kill()
        blood = __main__.Find("victimbloodb")
        if(blood):
            blood.Kill()
        cops = __main__.FindEntitiesByName("cop")
        for cop in cops:
            cop.Kill()
        victim = Find("victim")
        if(victim):
            victim.Kill()
        trigger = Find("murder_scene_trigger")
        if(trigger):
            trigger.Kill()

#PIER: called when the murder scene. Get it?
def murderSeen():
    if(G.Know_Murder == 0):
        G.Know_Murder = 1
        __main__.FindPlayer().SetQuest("Serial", 2)

#PIER: decides if rosa should direct the PC or not
def rosaDirections():
    if(G.Mercurio_Quest == 1):
        relay = Find("rosa_relay")
        if(relay):
            relay.Trigger()
        trigger = Find("rosa_trigger")
        if(trigger):
            trigger.Kill()

#PIER: removes the thin bloods at the appropriate story state, changed by wesp
def thinBloodsGone():
    if(G.Story_State >= 35):
        thinblood_killer = Find("thinblood_killer")
        if(thinblood_killer):
            thinblood_killer.Trigger()
        pc = __main__.FindPlayer()
        status = pc.GetQuestState("Lily")
        if(status == 2):
            pc.SetQuest("Lily", 5)
        elif(status == 3):
            pc.SetQuest("Lily", 6)
    if(G.Copper_Slayer or G.Copper_Uni == 2):
        copper = Find("Copper")
        if(copper):
            copper.Kill()
    if G.Patch_Plus == 1:
        gum = Find("gum")
        gumnode = Find("gumnode")
        if gum: gum.ScriptUnhide()
        if gumnode: gumnode.ScriptUnhide()

#PIER:  update "B Rated Writer"
def updateWriter():
    if (__main__.FindPlayer().GetQuestState("Writer") == 2):
        __main__.FindPlayer().SetQuest("Writer", 5)

#SANTAMONICA: used to determine if Bertram is in the oil tank or not, changed by wesp
def bertramOutOfHiding():
    if(G.Story_State >= 10 and not G.SM_Gone):
        G.SM_Gone = 1
        copcars = __main__.FindEntitiesByName("copcar")
        for copcar in copcars:
            copcar.Kill()
    npc = Find("Bertram")
    if(G.Tourette_Wins == 1 or G.Therese_Dead == 1 or G.Jeanette_Dead == 1):
        gate = Find("gasstationgate")
        pad = Find("padlock")
        if npc:
            pcon = Find("bertrams_computer_on")
            pcoff = Find("bertrams_computer_off")
            npc.ScriptUnhide()
            pcon.ScriptHide()
            pcoff.ScriptUnhide()
        gate.Unlock()
        if pad: pad.Unlock()
        knox = Find("Knox")
        if knox:
            if(G.Knox_Quest < 4 or G.Knox_Quest > 6):
                knox.ScriptHide()
            else:
                knox.ScriptUnhide()
    else:
        npc.ScriptHide()

#SANTAMONICA: tells the blue blood to go to the alley if he's dominated
def bluebloodToAlley():
#    camera = Find("blueblood_camera")
    if(G.Smblue_Dominated):
        blueblood = Find("SMblueblood")
        blueblood.WillTalk(0)
        blueblood.UseInteresting(1)
        #camera.StartShot()
        #script = Find("blue_blood_to_alley")
        #script.StartSchedule()
        #__main__.ScheduleTask(1.0, "__main__.FindEntityByName(\"player_alley_relay\").Trigger()")

#SANTAMONICA: puts the bum outside the haven on the first map load
def bumPlacement():
    triggers = FindList("prophet_trigger")
    for trigger in triggers:
        trigger.Enable()
    if(G.Haven_Bum == 0):
        bum = Find("havenbum")
        if bum: bum.ScriptUnhide()
        bum2 = Find("haven_bum_male")
        if bum2: bum2.ScriptHide()
        G.Haven_Bum = 1
        if(__main__.IsClan(__main__.FindPlayer(), "Ventrue")):
            if bum: bum.UseInteresting(1)
    else:
        bum = Find("havenbum")
        if bum: bum.Kill()
        bum2 = Find("haven_bum_male")
        if bum2: bum2.ScriptUnhide()

#SANTAMONICA: enacts the results of a conversation with Chunk
def chunkDialogueResults():
    chunk = Find("Chunk")
    if(G.Chunk_Open_Gallery == 0):
        G.Chunk_Called = G.Chunk_Called + 1
        chunk.UseInteresting(1)
        camera = Find("chunk_camera")
        if(G.Chunk_Befriend >= 2):
            relay = Find("criminal_disable")
            relay.Trigger()
            if(G.Chunk_Befriend == 3):
                G.Chunk_Open_Gallery = 1
                chunk.WillTalk(0)
                camera.StartShot()
                script = Find("chunk_unlock")
                script.BeginSequence()
                __main__.ScheduleTask(1.0, "__main__.FindEntityByName(\"follow_chunk_relay\").Trigger()")
            if(G.Chunk_Feed == 1):
                spawnGalleryKey()
            chunk.UseInteresting(1)
        elif(G.Chunk_Dominated == 1):
            G.Chunk_Open_Gallery = 1
            relay = Find("criminal_disable")
            relay.Trigger()
            chunk.WillTalk(0)
            camera.StartShot()
            script = Find("chunk_dominated")
            script.BeginSequence()
            __main__.ScheduleTask(1.0, "__main__.FindEntityByName(\"follow_chunk_relay\").Trigger()")
        elif(G.Chunk_Demented == 1):
            G.Chunk_Open_Gallery = 1
            relay = Find("criminal_disable")
            relay.Trigger()
            script = Find("chunk_dementated")
            script.BeginSequence()
            spawnGalleryKey()
            trigger = Find("Chunk_talk_alley_trigger")
            if(trigger):
                trigger.Disable()
            chunk.WillTalk(0)
            chunk.UseInteresting(0)
        else:
            relay = Find("criminal_enable")
            relay.Trigger()
            chunk.UseInteresting(1)
    elif(G.Chunk_Dominated == 2):
        chunk.WillTalk(0)
        script = Find("chunk_leaves")
        script.BeginSequence()

#SANTAMONICA: determines if chunk is present on SM, and what he is doing, changed by wesp
def chunkGone():
    chunk = Find("Chunk")
    if(G.Therese_Quest > 3 or G.Chunk_Dominated >= 1):
        if chunk: chunk.ScriptHide()
    elif(G.Chunk_Demented == 1):
        script = Find("chunk_dementated")
        script.BeginSequence()
        relay = Find("criminal_disable")
        relay.Trigger()
        trigger = Find("Chunk_talk_alley_trigger")
        trigger.Disable()
        if chunk:
            chunk.WillTalk(0)
            chunk.UseInteresting(0)

#SANTAMONICA: sets the cop patrolling
def copPatrol():
    cop = Find("patrol_cop")
    if cop:
        cop.SetupPatrolType("255 0 FOLLOW_PATROL_PATH_WALK")
        cop.FollowPatrolPath("s1 s2 s3 s4 s7 s8 s9 s10 s11 s12 s13 s14")
    cop = Find("patrol_cop_north")
    if cop:
        cop.SetupPatrolType("255 0 FOLLOW_PATROL_PATH_WALK")
        cop.FollowPatrolPath("n1 n2 n3 n4 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n1 n2 n3 n4")

#SANTAMONICA: sets quest status upon picking up Lilly's Diary
def diaryPickup():
    state = __main__.FindPlayer().GetQuestState("Lily")
    if(state != 10):
        G.E_Quest = 2
        __main__.FindPlayer().SetQuest("Lily", 2)

#SANTAMONIC: called when the player sees that someone else hit the Gallery
def galleryWitnessed():
    print "this function doesn't do anything anymore"
    G.Jeanette_Fire = 3
    #__main__.FindPlayer().SetQuest("Slashterpiece", 4)

#SANTAMONICA: Locks gimble after quest
def gimbleQuestDone():
    if(__main__.IsDead("Stan_Gimble")):
        #door = Find("basementdr")
        #door.Close()
        #door.Lock()
        intercom = Find("intercom_button")
        intercom.Lock()

#SANTAMONICA:
def initElysiumLoadTip():
    if(G.Elysium_Tip == 0):
        G.Elysium_Tip = 1
        G.Story_State_Save = G.Story_State
        G.Story_State = 2

#SANTAMONICA: open's gimintercomble's shop if the dialog allows it
def intercomDialog():
    if(G.Gimble_Open):
        door = Find("basementdr")
        door.Unlock()
        buzzer = Find("buzzer")
        buzzer.PlaySound()

#SANTAMONICA: updates the streets of Santa Monica for the gallery being attacked not by the player or afterwards, changed by wesp
def jeanetteRefused():
    if(G.Jeanette_Quest == 1):
        if(G.Bar_Broken == 0):
            inspect = Find("broken_bar_inspection")
            inspect.ScriptUnhide()
        chunk = Find("Chunk")
        if chunk: chunk.ScriptUnhide()
        trigger = Find("Chunk_talk_alley_trigger")
        trigger.ScriptUnhide()
    elif(G.Jeanette_Refuse >= 1 or G.Gallery_Slashed == 1):
        if(G.Jeanette_Fire < 3 and G.Story_State < 15):
            #__main__.FindPlayer().SetQuest("Slashterpiece", 3)
            trigger = Find("gallery_hit_trigger")
            trigger.Enable()
            trigger = Find("jeanette_refused_trigger")
            if trigger: trigger.Enable()
            spawnCopCarCalm(5)
            spawnCopCarCalm(6)
            cop = Find("Noir_Cop")
            cop.ScriptUnhide()
            relay = Find("criminal_disable")
            relay.Trigger()
            if (G.Chunk_Dominated == 0 and not __main__.IsDead("Chunk")):
                chunk = Find("Chunk")
                chunk.ScriptUnhide()
                G.Chunk_Demented = 1
                trigger = Find("Chunk_talk_alley_trigger")
                # Fixed Dheu
                if trigger:
                    trigger.Disable()
                script = Find("chunk_dementated")
                if script:
                    print("Chunk Dementated")
                    script.BeginSequence()
                chunk.WillTalk(0)
        elif(G.Noir_Done == 0):
            G.Noir_Done = 1
            chunk = Find("Chunk")
            if chunk: chunk.Kill()
            trigger = Find("jeanette_refused_trigger")
            if trigger: trigger.Kill()
            trigger = Find("gallery_hit_trigger")
            if trigger: trigger.Kill()
            cop = Find("Noir_Cop")
            if cop: cop.Kill()
            copcar = Find("cop_car_5")
            if copcar: copcar.Kill()
            copcar = Find("cop_car_6")
            if copcar: copcar.Kill()
            cops = FindList("stake_out_cop")
            for cop in cops:
                cop.Kill()
            relay = Find("criminal_disable")
            if relay: relay.Kill()
            trigger = Find("Chunk_talk_alley_trigger")
            if trigger: trigger.Kill()
            script = Find("chunk_dementated")
            if script: script.Kill()

#SANTAMONICA: Opens the junkyard
def junkyardOpen():
    if(G.Killer_Lucky == 1):
        gate = Find("junkyardgate")
        gate.Unlock()

#SANTAMONICA: Knox calls this when he dies to set quest status if necessary
def knoxDead():
    status = __main__.FindPlayer().GetQuestState("Knox Asian")
    if(status != 4 and status != 0):
        __main__.FindPlayer().SetQuest("Knox Asian", 8)

#SANTAMONICA: sends knox to the asylum at the appropriate story state
def knoxState():
    pc = __main__.FindPlayer()
    if(pc.clan == 5 and G.Knox_Nosferatu_Player == 0):
        G.Knox_Nosferatu_Player = 1
        teleport = Find("knox_clinic_teleport")
        teleport.Teleport()
        trigger = Find("knox_talk_trigger")
        if trigger: trigger.Kill()
        trigger = Find("knox_talk_trigger_nos")
        trigger.ScriptUnhide()
    if(G.Mercurio_Quest == 2 or __main__.IsDead("Knox")):
        knox = Find("Knox")
        if(knox):
            knox.Kill()

#SANTAMONICA: spawns the cop cars in without making the cops aggressive
def spawnCopCarCalm(i):
   ent = Find("cop_car_%i" % (i))
   ent.ScriptUnhide()
   ent = Find("calm_cop_front_%i" % (i))
   ent.Spawn()
   ent = Find("calm_cop_rear_%i" % (i))
   ent.Spawn()
   ent = Find("red%i" % (i))
   ent.TurnOn()
   ent = Find("blue%i" % (i))
   ent.TurnOn()
   ent = Find("cover_front_%i" % (i))
   ent.ScriptUnhide()
   ent = Find("cover_rear_%i" % (i))
   ent.ScriptUnhide()

#SANTAMONICA: places the gallery key in the world
def spawnGalleryKey():
    if(G.Gallery_Key == 0):
        chunk = Find("Chunk")
        center = chunk.GetCenter()
        point = (center[0] + 25, center[1] + 25, center[2])
        key = __main__.CreateEntityNoSpawn("item_k_gallery_noir_key", point, (0,0,0) )
        __main__.CallEntitySpawn(key)
        G.Gallery_Key = 1
        key.SetName("chunk_key")
        sparklies = __main__.CreateEntityNoSpawn("inspection_node", point, (0, 0, 0))
        sparklies.SetParent("chunk_key")
        __main__.CallEntitySpawn(sparklies)

#SANTAMONICA: summons taxi if the player is far enough in the game, changed by wesp
# Changed By CompMod
def taxi():
    if(G.Story_State == 5 and G.Mercurio_Blood_Clean == 0):
        G.Mercurio_Blood_Clean = 1
        bloodstains = FindList("blood")
        for stain in bloodstains:
            stain.Kill()
    if G.Story_State >= 5 and 5 != __main__.G._pcinfo["clan"]:
        # if G.Story_State >= 5 and not __main__.FindPlayer().IsClan("nosferatu"):
        taxi_driver = Find("cabbie")
        taxi_driver.ScriptUnhide()
        taxi = Find("taxi")
        taxi.ScriptUnhide()
        clip = Find("taxi_clip")
        clip.ScriptUnhide()
    if((G.Story_State >= 5 or __main__.IsDead("SMblueblood")) and G.Blueblood_Gone == 0):
        blueblood = Find("SMblueblood")
        if blueblood: blueblood.Kill()
        G.Blueblood_Gone = 1

#SANTAMONICA: sends the player to the warehouse if Bertram is ready to take them
def toWarehouse():
    if(G.Bertram_Ready == 2 and G.Story_State < 5):
        __main__.ChangeMap(2.5, "warehouselandmark", "warehouseteleport")

#SEWER: hides the ocean house from the sewer after the quest, changed by wesp
def oceanHouseQuest():
    if(G.Therese_Quest > 1):
        guy = Find("ManholeB7")
        guy.ScriptHide()

#SEWER: enables the map transition button
def sewerMapEnable():
    # Changed By CompMod
    # if G.Story_State >= 5 and __main__.FindPlayer().IsClan("nosferatu"):
    if G.Story_State >= 5 and 5 == __main__.G._pcinfo["clan"]:
        map = Find("sewer_map")
        map.Unlock()
#------------------------------------SAMEDI------------------------------
#SM_GALLERY: samedi boss activate disciplines; now disabled
#SAMEDI: samedi_1 cast zombies.         
def SamediCastSpellzombies():
    if(G.samedi_1_anger == 1):
        Find("samedi_cast_zombies").BeginSequence()
	__main__.ScheduleTask(0.1,"SamediCastZombies1()")

def SamediCastZombies1():
        Find("sound1_samedi_cast_zombies").PlaySound()
        Find("zombie_spawner_samedi").Spawn()
        Find("zombie_spawner1_samedi").Spawn()
	__main__.ScheduleTask(5.0,"SamediCastThanatosis1()")

#SAMEDI: samedi_1 cast thanatosis 4 level.... 
def SamediCastThanatosis1():
        Find("samedi_cast_thanatosis1").BeginSequence()
        Find("sound2_samedi_cast_thanatosis1").PlaySound()
        consoleutil.console("hidehud 1")
	__main__.ScheduleTask(0.1,"SamediCastThanatosis1helper1()")

def SamediCastThanatosis1helper1():
        pc=__main__.FindPlayer()
        pc.RemoveItem("item_w_fists")
        pc.GiveItem("item_w_mingxiao_spit")
        consoleutil.console("use item_w_mingxiao_spit")
	__main__.ScheduleTask(5.0,"SamediCastThanatosis1helper2()")

def SamediCastThanatosis1helper2():
        pc=__main__.FindPlayer()
        pc.RemoveItem("item_w_mingxiao_spit")
        pc.GiveItem("item_w_fists")
        consoleutil.console("hidehud 0")
        __main__.ccmd.holster=""
	__main__.ScheduleTask(5.0,"SamediCastThanatosis1helper3a()")

#SAMEDI: samedi_1 cast thanatosis 3 level 'dust to dust'....
def SamediCastThanatosis1helper3a():
        Find("samedi_cast_thanatosis2").BeginSequence()
        samedi1 = Find("samedi_1")
        samedi1.MakeInvincible(1)
#	__main__.ScheduleTask(1.45,"SamediCastThanatosis1helper3()")

def SamediCastThanatosis1helper3():
        samedi1 = Find("samedi_1")
        castsound3 = Find("sound3_samedi_cast_thanatosis2")
        castsound3.PlaySound()
        samedi1.SetModel("models/null.mdl")
        samedi1Clone=__main__.CreateEntityNoSpawn("npc_VHuman",samedi1.GetOrigin(),samedi1.GetAngles())
        samedi1Clone.SetName("samedi1Clone")
        __main__.CallEntitySpawn(samedi1Clone)
        samedi1Clone = __main__.FindEntityByName("samedi1Clone")
        if samedi1Clone:
            samedi1Clone.SetParent("samedi_1")
            samedi1Clone.SetOrigin(samedi1.GetOrigin())
            samedi1Clone.SetAngles(samedi1.GetAngles())
            samedi1Clone.SetModel("models/scenery/misc/skeleton/dead_skeleton_samedi.mdl")
	    __main__.ScheduleTask(5.0,"SamediCastThanatosis1helper4()")

def SamediCastThanatosis1helper4():
        samedi1 = Find("samedi_1")
        samedi1Clone = Find("samedi1Clone")
        samedi1.MakeInvincible(0)
        samedi1.SetModel("models/character/npc/common/samedi/samedi.mdl")
        samedi1Clone.ClearParent()
        samedi1Clone.Kill()

#SAMEDI: Samedi cast tanatosis compress. On end kill the player....       
def SamediCastCompress():
    pc=__main__.FindPlayer()
    samedi1 = Find("samedi_1")
    if(G.samedi_1_anger == 1):
        Find("samedi_Spell_Compress").BeginSequence()
	__main__.ScheduleTask(0.1,"SamediCastCompresshelper1()")

def SamediCastCompresshelper1():
    pc=__main__.FindPlayer()
    samedi1 = Find("samedi_1")
    if(G.samedi_1_dead == 1):
        pc=__main__.FindPlayer()
        pc.Bloodloss(0)
    else:
        Find("sound1_samediCastCompress").PlaySound()
        __main__.ScheduleTask(0.1,"SamediCastCompresshelper2()")

def SamediCastCompresshelper2():
        Find("compress_pc_start").BeginSequence()
        __main__.ScheduleTask(1.75,"SamediCastCompresshelper3()")

def SamediCastCompresshelper3():
        Find("compress_pc_loop").BeginSequence()
        __main__.ScheduleTask(2.15,"SamediCastCompresshelper4()")

def SamediCastCompresshelper4():
        Find("compress_pc_fall_sleep").BeginSequence()
        __main__.ScheduleTask(1.15,"SamediCastCompresshelper5()")

def SamediCastCompresshelper5():
        Find("sound2_samediCastCompress").PlaySound() 
        consoleutil.console("vdmg 95")
#------------------------------------SAMEDI END------------------------------
#BEACHHOUSE: Brian spawn shoulder pad
def BrianDeath():
    Brian = Find("Brian")
    center = Brian.GetCenter()
    point = (center[0], center[1], center[2] + 20)
    pad = __main__.CreateEntityNoSpawn("item_p_occult_obfuscate", point, (0,0,0) )
    pad.SetName("pad")
    sparklies = __main__.CreateEntityNoSpawn("inspection_node", point, (0,0,0) )
    sparklies.SetParent("pad")
    __main__.CallEntitySpawn(pad)
    __main__.CallEntitySpawn(sparklies)

#-------------------------------------------------------------------
#SABBAT HEAVEN: trigger change map sabbat taxi ride
def SabbatTaxi():
    consoleutil.console("thirdperson 1")
    pc=__main__.FindPlayer() 
    pcClone = Find("pc_clone_body")
    pcClone.SetModel(pc.model)
  

def SabbatTaxiEnter():
    __main__.ChangeMap(0.1, "dogs_enter_landmark_1", "trig_dogs_enter")

def SabbatTaxiExit():
    __main__.ChangeMap(0.1, "dogs2_taxi_landmark", "sabbat_taxiride_end")

#-------------------------------------------------------------------
#BASEMENT: old caln tzimisce kill Stan Gimble
def OldClanKillStan():
    pc=__main__.FindPlayer()
    clan = pc.clan
    if(clan == 4):
    	return
    	#Find("oldclan_kill_relay").Trigger()

def OldClanLookPC():
    __main__.FindPlayer().SetQuest("Oldknowledge", 1)
    __main__.FindPlayer().SetQuest("Oldclanblood", 1)

def OldClanOpen():
    Find("toolroom_relay").Trigger()

def OldClanRead():
    __main__.FindPlayer().SetQuest("Oldknowledge", 2)
    __main__.FindPlayer().SetQuest("Oldclanblood", 2)
    G.Koldunism_Level=2

#Gimble BOOM
def GimbleBoom():
    Find("GimbleExplosion").SetOrigin(Find("Stan_Gimble").GetOrigin())
    __main__.ScheduleTask(0.1,"GimbleBoom2()")
    __main__.ScheduleTask(0.05,"GimbleBoom3()")

def GimbleBoom2():
    Find("GimbleExplosion").Explode()

def GimbleBoom3():
    Gimble1=__main__.CreateEntityNoSpawn("prop_physics",Find("Stan_Gimble").GetOrigin(),Find("Stan_Gimble").GetAngles())
    Gimble1.SetName("Gimble1")
    Gimble1.SetModel("models/gibs/hgibstorso_prop.mdl")
    __main__.CallEntitySpawn(Gimble1)
    Gimble2=__main__.CreateEntityNoSpawn("prop_physics",Find("Stan_Gimble").GetOrigin(),Find("Stan_Gimble").GetAngles())
    Gimble2.SetName("Gimble2")
    Gimble2.SetModel("models/gibs/hgibslleg_prop.mdl")
    __main__.CallEntitySpawn(Gimble2)
    Gimble3=__main__.CreateEntityNoSpawn("prop_physics",Find("Stan_Gimble").GetOrigin(),Find("Stan_Gimble").GetAngles())
    Gimble3.SetName("Gimble3")
    Gimble3.SetModel("models/gibs/hgibslarm_prop.mdl")
    __main__.CallEntitySpawn(Gimble3)
    Gimble4=__main__.CreateEntityNoSpawn("prop_physics",Find("Stan_Gimble").GetOrigin(),Find("Stan_Gimble").GetAngles())
    Gimble4.SetName("Gimble4")
    Gimble4.SetModel("models/gibs/hgibsskull_prop.mdl")
    __main__.CallEntitySpawn(Gimble4)

#-------------------------------------------------------------------
#BASEMENT: create gargoyle
def GargoyleWerBloodCheck():
    container = Find("Rockbiter_statue")
    if container.HasItem("item_g_werewolf_bloodpack"):
	__main__.ScheduleTask(0.5,"GargoyleWerBloodCheck1()")

def GargoyleWerBloodCheck1():
    Find("Rockbiter_relay1").Trigger()

#BASEMENT: check gargoyle book on pedestal
def GargoyleBookCheck():
    container = Find("Rockbiter_pedestal")
    if container.HasItem("item_g_gargoyle_book"):
	__main__.ScheduleTask(0.5,"GargoyleBookCheck1()")

def GargoyleBookCheck1():
    Find("Rockbiter_relay2").Trigger()

#BASEMENT: check gargoyle talisman into the book
def GargoyleTalismanCheck():
    container = Find("Rockbiter_book")
    if container.HasItem("item_p_gargoyle_talisman"):
	__main__.ScheduleTask(0.5,"GargoyleTalismanCheck1()")

def GargoyleTalismanCheck1():
    Find("Rockbiter_relay3").Trigger()

#TATTOO: Gargoyle quest 
def GargoyleQuest1():
    __main__.FindPlayer().SetQuest("Gargoylequest", 1)

#BASEMENT: Gargoyle quest 
def GargoyleQuest2():
    __main__.FindPlayer().SetQuest("Gargoylequest", 2)
    Find("gargoyle_notes2_relay").Trigger()

def GargoyleQuest3():
    __main__.FindPlayer().SetQuest("Gargoylequest", 3)
    G.Gargoyle_Quest = 3

#-----------------------------
#PAWNSHOP_1: check clan when map load
def ClanWeaknessCheck():
    pc=__main__.FindPlayer()
    clan = pc.clan

    if (clan == 4 or clan == 6):
        Find("tzimisce_weakness_relay").Trigger()
    else:
        Find("not_tzimisce_relay").Trigger()
    	if (clan == 7):
            Find("nagaraja_weakness_relay").Trigger()


#-------------------------------------------------------------------
#DANE: check for dane boat
def boatcheck():
    pc = __main__.FindPlayer()
    state = pc.GetQuestState("Dane")
    if (state == 1 or state == 2):
        unhidetrig = Find("Relay_Unhide_Boat")
        unhidetrig.Trigger()
        if (state == 2):
            if(pc.HasItem("item_k_edane_key")):
                __main__.ScheduleTask(1.00, "__main__.FindPlayer().RemoveItem(\"item_k_edane_key\")")
            boatchangelevel = Find("boat_changelevel")
            boatchangelevel.ScriptHide()
    else:
        hidetrig = Find("Relay_Hide_Boat")
        hidetrig.Trigger()

#TJP: SEPT 15th I'm drunk. Hasn't this game shipped yet?
def TripStoryState():
    if (G.Story_State == 0):
        G.Story_State = 1

print "levelscript loaded"
