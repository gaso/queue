# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

def migrate(cr, installed_version):
    """
    Migración adaptada del formato OpenUpgradeLib al formato nativo de Odoo.
    """
    # Necesitamos crear el ambiente manualmente ya que no tenemos acceso a env directamente
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Remove cron garbage collector
    # Implementación nativa de delete_records_safely_by_xml_id
    xml_id = "queue_job.ir_cron_queue_job_garbage_collector"
    
    try:
        # Buscar el registro usando el XML ID
        record = env.ref(xml_id, raise_if_not_found=False)
        if record:
            # Eliminar el registro de forma segura
            record.unlink()
    except Exception as e:
        # Si hay algún error al eliminar, simplemente registrarlo
        # pero no detener la migración
        from logging import getLogger
        logger = getLogger(__name__)
        logger.warning(
            f"No se pudo eliminar el registro {xml_id}: {str(e)}"
        )
