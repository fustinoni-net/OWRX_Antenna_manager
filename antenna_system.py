import logging
from abc import ABC
from typing import Callable


class AntennaSystem(ABC):
    """
    Abstract base class for antenna systems.
    """

    class Antenna:
        """
        Class representing an antenna.
        """
        def __init__(self, name, antenna_id):
            self.name: str = name
            self.id: str = antenna_id

        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
            }

    def __init__(self):
        self.antenna_listener: list[Callable[[AntennaSystem.Antenna], None]]= []
        self.antennas: list[AntennaSystem.Antenna] = []
        self.current_antenna = None


    def get_available_antennas(self) -> list[Antenna]:
        """
        Get the list of available antennas.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def _switch_antenna(self, antenna):
        """
        Switch the antenna. To be reimplemented in subclasses.
        :param antenna:
        :return:
        """
        ...


    def set_default_antenna(self) -> None:
        """
        Set the default antenna.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_used_antenna(self) -> Antenna:
        raise NotImplementedError("This method should be overridden by subclasses.")


    def set_antenna_change_listener(self, antenna_has_changed: Callable[[Antenna], None]) -> None:
        """
        Notify about the antenna change.
        """
        self.antenna_listener.append(antenna_has_changed)


    def set_used_antenna(self, antenna: Antenna) -> None:
        """
        Get the used antenna.
        """
        if antenna in self.antennas:
            self._switch_antenna(antenna)
            self.current_antenna = antenna
            for listener in self.antenna_listener:
                listener(antenna)
            logging.info("AntennaSystem: Antenna switched to: %s", antenna.name)
        else:
            raise ValueError("Antenna not available in the system.")



class DummyAntennaSystem(AntennaSystem):
    def __init__(self):
        super().__init__()
        self.antennas = [
            self.Antenna(name="antenna1", antenna_id='1'),
            self.Antenna(name="antenna2", antenna_id='2'),
            self.Antenna(name="antenna3", antenna_id='3')
        ]


    def get_available_antennas(self) -> list[AntennaSystem.Antenna]:
        return self.antennas


    def set_default_antenna(self) -> None:
        self.set_used_antenna(self.antennas[0]) # Default to the first antenna
        logging.info("DummyAntennaSystem: Default antenna set to: %s", self.antennas[0].name)

    def get_used_antenna(self) -> AntennaSystem.Antenna:
        return self.current_antenna

    def set_antenna_change_listener(self, antenna_has_changed: callable) -> None:
        self.antenna_listener.append(antenna_has_changed)

    def _switch_antenna(self, antenna: AntennaSystem.Antenna):
        logging.log(logging.INFO, f"DummyAntennaSystem: Switching to antenna: {antenna.name}")
