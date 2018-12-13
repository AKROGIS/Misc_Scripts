REM use to move data from the new external hard drive at a park to a robo copy folder
REM this is required when there is a change to the robo copy portion of the PDS that is too large to robo
REM This must be run from inside a junction point to a remote server
REM i.e.
REM cd \tmp\RemoteServers\XDrive-YUGA\Mosaics\Statewide\DEMs
REM
mkdir SDMI_IFSAR.gdb
mkdir SDMI_IFSAR.Overviews
mkdir SDMI_IFSAR.Overviews\DSM.Overviews
mkdir SDMI_IFSAR.Overviews\DTM.Overviews
mkdir SDMI_IFSAR.Overviews\ORI.Overviews
mkdir SDMI_IFSAR.Overviews\ORI_SUP1.Overviews
mkdir SDMI_IFSAR.Overviews\ORI_SUP2.Overviews
mkdir SDMI_IFSAR.Overviews\ORI_SUP3.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.gdb\* SDMI_IFSAR.gdb
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\DSM.Overviews\* SDMI_IFSAR.Overviews\DSM.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\DTM.Overviews\* SDMI_IFSAR.Overviews\DTM.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\ORI.Overviews\* SDMI_IFSAR.Overviews\ORI.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\ORI_SUP1.Overviews\* SDMI_IFSAR.Overviews\ORI_SUP1.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\ORI_SUP2.Overviews\* SDMI_IFSAR.Overviews\ORI_SUP2.Overviews
copy ..\..\..\Extras\Trash\MosaicUpdate\SDMI_IFSAR.Overviews\ORI_SUP3.Overviews\* SDMI_IFSAR.Overviews\ORI_SUP3.Overviews
