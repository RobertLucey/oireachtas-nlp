import argparse
from random import sample

from textgenrnn import textgenrnn

from oireachtas_nlp import logger
from oireachtas_nlp.models.para import ExtendedParas
from oireachtas_nlp.utils import get_speaker_para_map, get_party_para_map


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--group-by', dest='group_by', type=str, required=True, choices=['member', 'party'])
    parser.add_argument('--prefix', dest='prefix', type=str, help='What text to start a sentence with. Generated text will continue the sentence')
    parser.add_argument('--only-groups', dest='only_groups', help='a csv of groups (party name / member name) to exclusively look for', type=str)
    parser.add_argument('--sample', dest='sample', type=int, default=1000, help='How many sentences of each group to sample')
    parser.add_argument('--num-epochs', dest='num_epochs', type=int, default=50)
    parser.add_argument('--generate-temp', dest='generate_temp', type=float, default=0.5, help='What temperature between 0 and 1 to generate text at (higher is more... creative)')
    parser.add_argument('--num-print-per-group', dest='num_print_per_group', type=int, default=100, help='How many lines to generate for each group')
    args = parser.parse_args()

    only_groups = None
    if args.only_groups is not None:
        only_groups = args.only_groups.split(',')

    if args.group_by == 'party':
        for party, paras in get_party_para_map(only_groups=only_groups).items():
            extended_paras = ExtendedParas(data=paras)
            texts = extended_paras.text_obj.quick_sentences

            if len(texts) < args.sample:
                logger.warning(f'{party} has too few sentences to process. Consider lowering --sample')
                continue

            texts = sample(texts, args.sample)

            logger.info(f'Begin training: {party}')

            textgen = textgenrnn()
            textgen.train_on_texts(texts, num_epochs=args.num_epochs)
            textgen.generate(n=args.num_print_per_group, prefix=args.prefix, temperature=args.generate_temp, progress=False)

    else:
        for speaker, paras in get_speaker_para_map(only_groups=only_groups).items():
            extended_paras = ExtendedParas(data=paras)
            texts = extended_paras.text_obj.quick_sentences

            if len(texts) < args.sample:
                logger.warning(f'{speaker} has too few sentences to process. Consider lowering --sample')
                continue

            texts = sample(texts, args.sample)

            logger.info(f'Begin training: {speaker}')

            textgen = textgenrnn()
            textgen.train_on_texts(texts, num_epochs=args.num_epochs)
            textgen.generate(n=args.num_print_per_group, prefix=args.prefix, temperature=args.generate_temp, progress=False)


if __name__ == '__main__':
    main()
