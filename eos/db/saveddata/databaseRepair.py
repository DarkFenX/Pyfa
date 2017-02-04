# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import sqlalchemy
from logbook import Logger
logging = Logger(__name__)


class DatabaseCleanup:
    def __init__(self):
        pass

    @staticmethod
    def OrphanedCharacterSkills(saveddata_engine):
        # Finds and fixes database corruption issues.
        logging.debug("Start databsae validation and cleanup.")

        # Find orphaned character skills.
        # This solves an issue where the character doesn't exist, but skills for that character do.
        # See issue #917
        try:
            logging.debug("Running database cleanup for character skills.")
            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM characterSkills "
                                               "WHERE characterID NOT IN (SELECT ID from characters)")
            row = results.first()

            if row and row['num']:
                delete = saveddata_engine.execute("DELETE FROM characterSkills WHERE characterID NOT IN (SELECT ID from characters)")
                logging.error("Database corruption found. Cleaning up {0} records.", delete.rowcount)

        except sqlalchemy.exc.DatabaseError:
            logging.error("Failed to connect to database.")

    @staticmethod
    def OrphanedFitDamagePatterns(saveddata_engine):
        # Find orphaned damage patterns.
        # This solves an issue where the damage pattern doesn't exist, but fits reference the pattern.
        # See issue #777
        try:
            logging.debug("Running database cleanup for orphaned damage patterns attached to fits.")

            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM fits WHERE damagePatternID NOT IN (SELECT ID FROM damagePatterns) OR damagePatternID IS NULL")
            row = results.first()

            if row and row['num']:
                # Get Uniform damage pattern ID
                query = saveddata_engine.execute("SELECT ID FROM damagePatterns WHERE name = 'Uniform'")
                rows = query.fetchall()

                if len(rows) == 0:
                    logging.error("Missing uniform damage pattern.")
                elif len(rows) > 1:
                    logging.error("More than one uniform damage pattern found.")
                else:
                    uniform_damage_pattern_id = rows[0]['ID']
                    update = saveddata_engine.execute("UPDATE 'fits' SET 'damagePatternID' = ? "
                                                      "WHERE damagePatternID NOT IN (SELECT ID FROM damagePatterns) OR damagePatternID IS NULL",
                                                       uniform_damage_pattern_id)
                    logging.error("Database corruption found. Cleaning up {0} records.", update.rowcount)
        except sqlalchemy.exc.DatabaseError:
            logging.error("Failed to connect to database.")

    @staticmethod
    def OrphanedFitCharacterIDs(saveddata_engine):
        # Find orphaned character IDs. This solves an issue where the character doesn't exist, but fits reference the pattern.
        try:
            logging.debug("Running database cleanup for orphaned characters attached to fits.")
            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM fits WHERE characterID NOT IN (SELECT ID FROM characters) OR characterID IS NULL")
            row = results.first()

            if row['num']:
                # Get All 5 character ID
                query = saveddata_engine.execute("SELECT ID FROM characters WHERE name = 'All 5'")
                rows = query.fetchall()

                if len(rows) == 0:
                    logging.error("Missing 'All 5' character.")
                elif len(rows) > 1:
                    logging.error("More than one 'All 5' character found.")
                else:
                    all5_id = rows[0]['ID']
                    update = saveddata_engine.execute("UPDATE 'fits' SET 'characterID' = ? "
                                                      "WHERE characterID not in (select ID from characters) OR characterID IS NULL",
                                                       all5_id)
                    logging.error("Database corruption found. Cleaning up {0} records.", update.rowcount)
        except sqlalchemy.exc.DatabaseError:
            logging.error("Failed to connect to database.")
