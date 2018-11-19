#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging

game = hlt.Game()

game.ready("Telos")

logging.info("Player ID: {}.".format(game.my_id))

while True:
    game.update_frame()

    me = game.me
    game_map = game.game_map
    command_queue = []
    ship_status = {}

    for ship in me.get_ships():
        if (
            game_map[ship.position].halite_amount < constants.MAX_HALITE / 10
            or ship.is_full
        ):
            command_queue.append(
                ship.move(
                    random.choice(
                        [
                            Direction.North,
                            Direction.South,
                            Direction.East,
                            Direction.West,
                        ]
                    )
                )
            )
        else:
            command_queue.append(ship.stay_still())

        # Gather dropoffs #
        dropoffs = me.get_dropoffs()
        dropoffs.append(me.shipyard)
        for dropoff in dropoffs:
            dist = game_map.calculate_distance(ship.position, dropoff.position)

            # Ship Organiser #
            if ship.id not in ship_status:
                ship_status[ship.id] = "Randomly Moving"
            elif me.halite_amount >= 4000 and dist > 30:
                ship_status[ship.id] = "Spawning DropOff"
            elif ship.halite_amount >= 200:
                ship_status[ship.id] = "Dropping Halite off"

            logging.info(
                "Ship '{}' is currently '{}' carrying '{}' halite.".format(
                    ship.id, ship_status[ship.id], ship.halite_amount
                )
            )

    # End Game #
    if (
       game.turn_number <= 200
      and me.halite_amount >= constants.SHIP_COST
       and not game_map[me.shipyard].is_occupied
    ):
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)

