# -*- coding: utf-8 -*-
{
    "name": "Google Drive Odoo Integration",
    "version": "11.0.1.1.3",
    "category": "Document Management",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/11.0/google-drive-odoo-integration-280",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "cloud_base"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {
        "python": []
},
    "summary": "The tool to automatically synchronize Odoo attachments with Google Drive files in both ways",
    "description": """
    Odoo document system is clear and comfortable to use. However, it is not designed to work with files as Google Drive does. To process attachments users need to download a file, to change it, and to upload back. Documents are not synced locally and Odoo doesn't have powerful previewers and editors like Google Documents or Google Spreadsheets. Google Drive doesn't have such disadvantages. This is the tool to integrate Google Drive features into your Odoo business work flow. The app automatically stores all Odoo attachments in Google Drive and provides an instant access to them via web links. In such a way users work with files comfortably in Google Drive, while the results are fully available in Odoo.

    The module recovers the 'Attachments' menu for any Odoo document removed in Odoo 12
    Synchronization is <strong>bilateral</strong>. All Odoo attachments are put in Google Drive regularly. Google Drive files create attachments in Odoo in case they are placed in a correct folder. Look at the sections <a href='#direct_sync'>From Odoo to Google Drive</a> and <a href='#backward_sync'>From Google Drive to Odoo</a>
    Integration is <strong>automatic</strong> in both ways. Based on scheduled jobs, Odoo send attachments to Google Drive and retrieve files from there
    <strong>Any Odoo</strong> document might be synced: customers, opportunities, sale or purchase orders, tasks or issues, employees or users, etc. You decide by your own which records should be in Google Drive, and which should be left in Odoo
    Synchronization works both for <strong>individual drives</strong> and <strong>team drives</strong> (Google Suite business and enterprise tariffs). In the latter case the root folder Odoo is place within a chosen team drive, in the first case - within a current user drive
    All synced files are easily accessible though clicking on an attachment. Odoo automatically redirects you to a <strong>file previewer</strong>. Among others it might be Google Documents and Google Spreadsheets. Besides, you might open a whole document folder by clicking on 'Open folder' on the attachment widget
    All sync activities might be logged. Control over files and folders creations, moves, name changes and removals. Just turn on the option 'Log sync activities' and access history through the button 'Sync logs'
    <i><strong><span style="color: #483d8b">New</span></strong></i> For each document of this type you may create a default directories' structure. When this folder is firstly synced, Odoo would generate default folders. For example, for all employees you may have pre-defined folders 'Scans', 'Scans/Official', 'Photos', etc.
    The tool is compatible with Odoo reporting and mailing apps. If such an app faces a synced file, it retrieves a real content from Google Drive. In particular, the reports 'always reload' feature and messages & mass mailing attachments work properly
    Integration is based on a single user endpoint. It means that you should login in Google Drive only once. Afterwards for integrations Odoo would use that credentials disregarding an actual Odoo user. <strong>Make sure</strong>, however, that real Odoo users have an access to Google Drive to open URLs linked to their attachments
    # <a name='direct_sync'></a>  From Odoo to Google Drive
    Direct synchronization has 2 prime aims:
<ul>
<li>Prepare and keep updated folders' structure in Google Drive</li>
<li>Upload new attachments to a correct folder</li>
</ul>
<strong>Folders</strong>
<p style="font-size:18px">
Odoo creates a convenient directory structure in Google Drive: Odoo / Document type name / Document name / Files, where:
<ul>
<li><i>Odoo</i> is a central directory for Odoo Sync in your Drive.</li>
<li><i>Document type</i> is a synced Odoo model, for example, 'Sale orders', 'Opportunities', 'Customers' 
<ul>
<li>You select document types by yourself. It might be <strong>any document type</strong></li>
<li>Moreover, you might have <strong>a few folders for a single document type</strong>. Use Odoo domains to have not global 'Partners, but 'Customers' and 'Suppliers', not just 'Sale orders' but 'Commercial offers', 'To deliver', and 'Done orders'</li>
<li>With each sync Odoo would try to update document types' folders. Add a new document type at any moment. It will appear in Google Drive with a next sync</li>

<li>You are welcome to introduce or change document types folder names at any moment in Odoo. Take into account: renaming in Google Drive will be recovered to Odoo names</li>
<li>If you remove a model from integration, it will <strong>not</strong> be deleted from Google Drive to keep already synced files safe. However, new documents of this type would not be synced</li>
<li>In case you removed a directory in Google Drive, but it is still configured in Odoo, with a next sync a folder structure is going to be recovered (not files, surely).</li>
</ul>
</li>
<li><i>Document</i> is an exact object to sync. For instance, 'Agrolait' or 'SO019'
<ul>
<li>Documents are synced in case they relate to a synced document type and satisfy its filters. For example, you are not obliged to sync all partners, you may integrate only 'Customers' and 'Vendors' or only 'Companies', not 'Contacts'</li>
<li>Odoo would generate a folder in Google Drive for each suitable document even for documents without attachments. It is needed for a backward sync to easily add new files</li>
<li>Google Drive folder name equals a real document name. It relies upon Odoo name_get method. Thus, Odoo 'Michael Fletcher' (a contact of 'Agrolait') would be Google Drive 'Agrolait, Michael Fletcher'</li>
<li>If an exact document changes its document type (e.g. a quotation is now confirmed), Odoo will  automatically relocate its related folder to a proper parent directory (in the example: from 'Commercial offers' to 'To deliver')</li>
<li>In case a document relates to a few types (for instance, you have 'Vendors' and 'Customers', while Agrolait is both), this document folder would be put into the most prioritized document type. A document type priority is higher as closer to the top in Odoo interfaces it is</li>
<li>If an Odoo document is removed, the next sync will remove a corresponding Google Drive directory</li>
<li>In case you remove a directory in Google Drive, but it still exists in Odoo, Google Drive folder structure would be recovered (while files would be unlinked in both Odoo and Google Drive)</li>
<li>Folders renaming in Google Drive will be replaced with Odoo names, Odoo document names are  more important</li>
</ul>
</li>
<li><i>Files</i> are real files taken from Odoo attachments</li>
</ul>
</p>
<p style="font-size:18px">
The resulted path would be, for example, 'Odoo / Quotations / SO019 / commercial offer.png'.
</p>
<p style="font-size:18px">
The only exclusion of the rule are <i>stand alone attachments</i> which do not relate to any Odoo documents (their document type is 'ir.attachment'). Such attachments' path is 'Odoo / Stand Alone Attachments / image.png'.
</p>
<p style="font-size:18px">
The very first sync might take quite a long, since a lot of folders should be created. Afterwards, it would be much faster. However, it is not recommended to make sync too frequent: once an hour seems quite good for large files.
</p>
<strong>Files</strong>
<p style="font-size:18px">
With each direct sync, Odoo tries to find not yet synced attachments. If such attachments suit any document type to sync, a file will be uploaded to Google Drive to a proper folder. In Odoo such attachments will become of 'url' type. It means that a file is not any more kept in Odoo server space, but now it is in Google Drive. Until sync is done, Odoo attachment remains binary and stores an actual file. Such approach helps Odoo to work faster.
</p>
<p "font-size:18px">
Clicking on such attachment leads you to a file previewer / editor in Google Drive. Depending on your Google Drive configurations it might be Google Documents, Google Spreadsheets, PDF previewer, etc. Anyway  changes to file contents in Google Drive are available in Odoo at the same moment. 
</p>
<p style="font-size:18px">
If you unlinked an attachment from Odoo, it would be deleted in Google Drive as well.
</p>
<p style="font-size:18px">
Take into account that file names should be managed in Google Drive: each backward sync would recover Google Drive names, Odoo is here less important.
</p>
    # <a name='backward_sync'></a>  From Google Drive to Odoo
    Backward integration aims to sync new files from Google Drive to Odoo:
<ul>
<li>If a new file is added to a proper document folder (e.g. to 'Odoo / Customers / Agrolait'), the same attachment will be added to Odoo document (in the example – to 'Agrolait')</li>
<li>In document folders you can put not only files but also <i>child folders</i>. In that case a link for this folder (not its content) is kept in attachments</li>
<li>In case you rename a file in Google Drive, it will be renamed in Odoo as well</li>
<li>Files' removal from Google Drive leads to related Odoo attachments' removal</li>
<li>If you move a file to another document folder, in Odoo a related attachment would be re-attached to this new document. Take into account: if you move a file for a not document folder, in Odoo attachment will be deleted as it has been removed from Google Drive</li>
<li>If you deleted a document type or a document folder, their child files are deleted as well. Thus, Odoo would remove related attachments. The folders, however, will be recovered with a next direct sync. Folders' move to another directory is also considered as a removal. Avoid such situations by following the simple rule: folders are managed mostly by Odoo, files – mostly by Google Drive.</li>
</ul>
<p style="font-size:18px">
Backward Google Drive sync might take quite much time, since each folder should be checked (the more folders, the more time the backward sync requires). It is recommended to make frequency oftener than once an hour or two hours.
</p>
    # <a name='details'></a>  Misc peculiarities
    <ul>
<li>Take into account that files or folders deleted in Google Drive are really deleted only when you clean trash. Otherwise, such files still exist and would be reflected in Odoo</li>
<li>Try to avoid the following symbols in folders' and files' names: *, ?, ", ', :, &lt;, &gt;, |, +, %, !, @, \, /,.  Direct sync will replace such symbols with '-'. It is done to avoid conflicts with file systems.</li>
</ul>
    Fast access to Google Drive files and folders
    Synced files are simply found in Google Drive. Add unlimited number of files or folders here
    Choose document types to be synced
    Document type might have a few folders based on filters
    All document types are in the root directory 'Odoo'
    Document types' folders
    All document of this type has an own folder
    Logged synchronisation activities
    Default folders for this document types to be created while firstly synced
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "264.0",
    "currency": "EUR",
}