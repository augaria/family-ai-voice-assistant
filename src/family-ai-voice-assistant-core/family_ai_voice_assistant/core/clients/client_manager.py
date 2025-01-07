from typing import Type, TypeVar, List

from ..utils.global_instance_manager import GlobalInstanceManager


T = TypeVar('T')


class ClientManager(GlobalInstanceManager):

    def get_client(self, client_type: Type[T]) -> T:
        client_list = self.get_instance(client_type)
        if not client_list or len(client_list) == 0:
            return None
        return client_list[0]

    def get_all_clients(self, client_type: Type[T]) -> List[T]:
        return self.get_instance(client_type)

    def get_instance(
        self,
        client_type: Type[T]
    ) -> List[T]:
        return super()._get_instance(
            identifier=client_type
        )

    def _create_instance(self) -> List[T]:
        return []

    def register_client(self, client_type: Type[T], instance: T):
        if instance is None:
            return
        client_list: List = super()._get_instance(
            identifier=client_type
        )
        client_list.append(instance)
        super()._add_instance(client_type, client_list)
