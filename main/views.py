from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from main.models import Clients, Projects, CostTypes, Costs


class CostExplorerView(generics.ListAPIView):
    clients = []
    projects = []
    store = {}

    def get_queryset(self):
        pass

    def set_clients(self, clients_query):
        for client_id in clients_query:
            filtered_client = Clients.objects.filter(id=client_id)
            if filtered_client:
                self.clients.append(filtered_client[0])

    def set_projects(self, client_id, projects_query):
        for project_id in projects_query:
            filtered_project = Projects.objects.filter(id=project_id, client_id=client_id)
            if filtered_project:
                self.projects.append(filtered_project[0])

    def build_store(self, project, all_cost_types):
        for cost_type in all_cost_types:
            cost_type_amount = Costs.objects.filter(cost_type_id=cost_type.id, project_id=project.id)
            if cost_type_amount:
                cost_type_amount = cost_type_amount[0].amount
            if cost_type.parent_cost_type_id in self.store:
                self.store[cost_type.parent_cost_type_id].append({'id': cost_type.id, 'name': cost_type.name,
                                                                  'amount': cost_type_amount})
            else:
                self.store[cost_type.parent_cost_type_id] = [{'id': cost_type.id, 'name': cost_type.name,
                                                              'amount': cost_type_amount}]

    def get_cost_breakdown(self, stop_if_id_in, current, current_amount, results, return_check):
        if current not in self.store and str(current) in stop_if_id_in:
            return [], True, current_amount
        elif current not in self.store and not bool(stop_if_id_in):
            return [], True, current_amount
        elif current not in self.store:
            return 'stop', False, 0
        current_list = self.store[current]
        total_amount = 0
        for cost_type in current_list:
            if str(current) not in stop_if_id_in:
                breakdown, new_return_check, amount = self.get_cost_breakdown(stop_if_id_in, cost_type['id'],
                                                                              cost_type['amount'], [], False)
                if return_check or new_return_check:
                    return_check = True
            else:
                return_check = True
                breakdown = []
                amount = cost_type['amount']
            if breakdown == 'stop':
                continue
            total_amount += amount
            results.append({'id': cost_type['id'], 'name': cost_type['name'], 'amount': amount, 'breakdown': breakdown})
        # if any child node wants to return
        if return_check is True:
            return results, True, total_amount
        else:
            return 'stop', False, 0

    def get(self, request, *args, **kwargs):
        # get query params
        clients_query = request.GET.getlist('clients[]')
        projects_query = request.GET.getlist('projects[]')
        cost_types_query = request.GET.getlist('cost_types[]')
        results = []

        self.clients.clear()
        self.projects.clear()
        self.store.clear()

        # get the clients for the given client id's in query params
        if clients_query:
            self.set_clients(clients_query)
        else:
            self.clients.extend(Clients.objects.all())  # for default test case i.e when path is /cost-explorer
            # with no params or client_id's not given at all

        for idx, client in enumerate(self.clients):
            if projects_query:
                self.set_projects(client.id, projects_query)
            else:
                projects_all_set = Projects.objects.all()
                self.projects.extend(projects_all_set.filter(client_id=client.id))

            results.append({'id': client.id, 'name': client.name, 'amount': 0, 'breakdown': []})
            total_cost_all_projects = 0

            for project in self.projects:
                project_json = {'id': project.id, 'name': project.title, 'amount': 0, 'breakdown': []}
                stop_if_id_in = set(cost_types_query) if cost_types_query else {}

                # build a dictionary in the pattern - parent_cost_type_id: [cost_type_ids..] i.e
                # { Null:[1,2,3], 1:[4,5,6], 2:[7,8,9], 3:[10,11], 4:[12,13]...}
                self.build_store(project, CostTypes.objects.all())

                # traverse recursively through the dictionary and get all child costs
                costs_breakdown, ignore, total_amount = self.get_cost_breakdown(stop_if_id_in, None, 0, [], False)

                project_json['breakdown'].append(costs_breakdown)
                project_json['amount'] = total_amount
                total_cost_all_projects += total_amount
                results[idx]['breakdown'].append(project_json)
                self.store.clear()
            results[idx]['amount'] = total_cost_all_projects
            self.projects.clear()

        # remove redundant clients with no further breakdowns after filtering
        final_res = []
        for idx, client in enumerate(results):
            if client['breakdown']:
                final_projects = []
                for idy, project in enumerate(client['breakdown']):
                    if not project['breakdown'][0] == 'stop':
                        final_projects.append(project)
                client['breakdown'] = final_projects
                if client['breakdown']:
                    final_res.append(client)

        del results
        return Response(final_res)

