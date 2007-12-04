"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-28
"""

from yadsel.core import *

class Version1(Version):
    version_number = 1

    def up(self):
        CreateTable('central_relacionamento',
                id = Integer(autoincrement=True, primary_key=True),
                dono_id = Integer(references=ForeignKey('auth_user', 'id')),
                amigo_id = Integer(references=ForeignKey('auth_user', 'id')),
                tipo = Char(1, default='P'),
            ).append_to(self)

        CreateTable('central_publicacaoacesso',
                id = Integer(autoincrement=True, primary_key=True),
                dono_id = Integer(references=ForeignKey('auth_user', 'id')),
                publicacao_id = Integer(references=ForeignKey('central_relacionamento', 'id')),
                data_criacao = DateTime(),
                interessa = Boolean(default=False),
                visualiza = Boolean(default=False),
                edita = Boolean(default=False),
                recomenda = Boolean(default=False),
                tipo = Char(1, default='P'),
            ).append_to(self)

        AlterTable('central_userinfo',
                RenameColumn('dono_id', 'user_id', Integer()),
                Add('moderador_id', Integer(required=False, references=ForeignKey('auth_user', 'id'))),
                Add('tipo', Char(1, default='P')),
            ).append_to(self)

        Update('central_userinfo',
                Set(tipo='C'),
                Where(e_comunidade=1),
            ).append_to(self)

        AlterTable('central_userinfo',
                DropColumn('e_comunidade'),
            ).append_to(self)

        AlterTable('central_publicacao',
                Add('tipo', Char(1, default='D')),
            ).append_to(self)

        Update('central_publicacao',
                Set(tipo='F'),
                Where(imagem__isnull=False),
            ).append_to(self)

        Insert('central_relacionamento',
                Select('central_userinfo_amigos a JOIN central_userinfo ui ON a.userinfo_id = ui.id',
                    dict(
                        dono_id = 'ui.user_id',
                        amigo_id = 'a.user_id',
                        tipo = 'A'
                        ),
                    ),
            ).append_to(self)

        CreateIndex(
                'idx_central_publicacao_tipo',
                'central_publicacao',
                ('tipo',)
            ).append_to(self)

    def down(self):
        DropIndex(
                'idx_central_publicacao_tipo',
                'central_publicacao'
            ).append_to(self)

        #DropTable('central_publicacaoacesso').append_to(self)
        #DropTable('central_relacionamento').append_to(self)

