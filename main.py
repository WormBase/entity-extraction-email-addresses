import argparse
import logging

from wbtools.db.generic import WBGenericDBManager
from wbtools.literature.corpus import CorpusManager

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Entity Extraction Pipeline - Email Addresses")
    parser.add_argument("-N", "--db-name", metavar="db_name", dest="db_name", type=str)
    parser.add_argument("-U", "--db-user", metavar="db_user", dest="db_user", type=str)
    parser.add_argument("-P", "--db-password", metavar="db_password", dest="db_password", type=str, default="")
    parser.add_argument("-H", "--db-host", metavar="db_host", dest="db_host", type=str)
    parser.add_argument("-w", "--tazendra-ssh-username", metavar="tazendra_ssh_user", dest="tazendra_ssh_user",
                        type=str)
    parser.add_argument("-z", "--tazendra_ssh_password", metavar="tazendra_ssh_password", dest="tazendra_ssh_password",
                        type=str)
    parser.add_argument("-l", "--log-file", metavar="log_file", dest="log_file", type=str, default=None,
                        help="path to log file")
    parser.add_argument("-L", "--log-level", dest="log_level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                        'CRITICAL'], default="INFO",
                        help="set the logging level")
    parser.add_argument("-m", "--max-num-papers", metavar="max_num_papers", dest="max_num_papers", type=int)

    args = parser.parse_args()
    logging.basicConfig(filename=args.log_file, level=args.log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s:%(message)s')

    cm = CorpusManager()
    db_manager = WBGenericDBManager(dbname=args.db_name, user=args.db_user, password=args.db_password,
                                    host=args.db_host)
    already_extracted_ids = db_manager.get_paper_ids_with_email_addresses_extracted()
    cm.load_from_wb_database(args.db_name, args.db_user, args.db_password, args.db_host,
                             tazendra_ssh_user=args.tazendra_ssh_user, tazendra_ssh_passwd=args.tazendra_ssh_password,
                             max_num_papers=args.max_num_papers, exclude_ids=already_extracted_ids, load_bib_info=False,
                             load_curation_info=False)
    for paper in cm.get_all_papers():
        paper.extract_all_email_addresses_from_text_and_write_to_db()
        logger.info("Extracted email address from paper " + paper.paper_id)


if __name__ == '__main__':
    main()
