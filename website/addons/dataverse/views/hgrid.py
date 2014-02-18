import time

from website.project.decorators import must_be_contributor_or_public
from website.project.decorators import must_have_addon
from website.util import rubeus

import hurry


def dataverse_hgrid_data(node_settings, user, contents=False, **kwargs):

    # Quit if no study linked
    hdl = node_settings.study_hdl
    if hdl == "None":
        return

    # connection = node_settings.user_settings.connect(
    #     node_settings.dataverse_username,
    #     node_settings.dataverse_password
    # )

    can_edit = True # TODO: Validate user

    # TODO: Add upload / fetch URLs
    # TODO: Expose get contents view function and route

    permissions = {
        'edit': can_edit,
        'view': True
    }

    urls = {
        'upload': node_settings.owner.api_url + 'dataverse/file/',
        'fetch': node_settings.owner.api_url + 'dataverse/hgrid/',
        'branch': node_settings.owner.api_url + 'dataverse/hgrid/root/',
    }

    return rubeus.build_addon_root(
        node_settings,
        'Dataverse: {0}/{1} {2}'.format(
            node_settings.dataverse_username, node_settings.dataverse, node_settings.study,
        ),
        urls=urls,
        permissions=permissions,
        extra=None,
    )


# TODO: Can this be combined with dataverse_hgrid_data?
@must_be_contributor_or_public
@must_have_addon('dataverse', 'node')
def dataverse_root_folder_public(*args, **kwargs):

    node_settings = kwargs['node_addon']

    return dataverse_hgrid_data(node_settings)


@must_be_contributor_or_public
@must_have_addon('dataverse', 'node')
def dataverse_hgrid_data_contents(**kwargs):

    node_settings = kwargs['node_addon']

    connection = node_settings.user_settings.connect(
        node_settings.dataverse_username,
        node_settings.dataverse_password
    )

    info = [node_settings.user_settings]

    study = connection.get_dataverses()[int(node_settings.dataverse_number)].get_study_by_hdl(node_settings.study_hdl)

    for f in study.get_files():

        item = {
            rubeus.KIND: rubeus.FILE,
            'name': f.name,
            'urls': { # TODO: Get some real URLs
                'view': node_settings.owner.api_url + 'dataverse/file/' + (f.fileId or ''),
                'download': node_settings.owner.api_url + 'dataverse/hgrid/' + (f.fileId or ''),
                'delete': node_settings.owner.api_url + 'dataverse/hgrid/root/',
            },
            'permissions': {
                'view': True,
                'edit': True, # TODO: Validate

            },
            'size': [
                    float(0), # TODO: Implement file size (if possible?),
                    hurry.filesize.size(0, system=hurry.filesize.alternative)
            ],
            'dates': { # TODO: Real times
                'modified': [
                    time.mktime(node_settings.study_hdl.date_modified.timetuple()),
                    node_settings.study_hdl.date_modified.strftime('%Y/%m/%d %I:%M %p')
                ],
            }
        }
        info.append(item)

    return info
