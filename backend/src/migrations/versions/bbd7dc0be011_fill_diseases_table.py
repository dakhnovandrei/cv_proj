"""fill diseases table

Revision ID: bbd7dc0be011
Revises: 3d94fb657ca6
Create Date: 2025-12-09 21:11:35.754650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = 'bbd7dc0be011'
down_revision: Union[str, Sequence[str], None] = '3d94fb657ca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

disease_data = [
    {
        "disease_name": 'Apple Scab Leaf',
        "recommendation": 'Удалите и сожгите пораженные листья и плоды. Обрабатывайте медьсодержащими фунгицидами до и после цветения. Осенью уничтожьте растительные остатки. Проводите прореживающую обрезку для вентиляции. Выбирайте устойчивые сорта.'
    },
    {
        "disease_name": 'Apple leaf',
        "recommendation": 'Полностью здоровый лист яблони.'
    },
    {
        "disease_name": 'Apple rust leaf',
        "recommendation": 'Удалите листья с оранжевыми пятнами. Не сажайте рядом с можжевельником. Обработайте медьсодержащими фунгицидами после цветения. Осенью перекопайте приствольный круг. Весной используйте бордосскую жидкость.'
    },
    {
        "disease_name": 'Bell_pepper leaf spot',
        "recommendation": 'Удалите больные листья, обеспечьте вентиляцию. Поливайте только под корень. Обработайте «Фитоспорином» или медьсодержащими препаратами. Мульчируйте почву. Соблюдайте севооборот.'
    },
    {
        "disease_name": 'Bell_pepper leaf',
        "recommendation": 'Полностью здоровый лист болгарского перца.'
    },
    {
        "disease_name": 'Blueberry leaf',
        "recommendation": 'Полностью здоровый лист голубики.'
    },
    {
        "disease_name": 'Cherry leaf',
        "recommendation": 'Полностью здоровый лист вишни.'
    },
    {
        "disease_name": 'Corn Gray leaf spot',
        "recommendation": 'Соблюдайте севооборот. Используйте устойчивые гибриды. Уничтожайте послеуборочные остатки. Применяйте фунгициды при вспышке. Избегайте густых посевов.'
    },
    {
        "disease_name": 'Corn leaf blight',
        "recommendation": 'Уничтожьте зараженные остатки после урожая. Выбирайте устойчивые гибриды. Обеспечьте пространство для проветривания. Обработайте фунгицидом при первых признаках. Сбалансируйте подкормки.'
    },
    {
        "disease_name": 'Corn rust leaf',
        "recommendation": 'Обработайте фунгицидом при первых признаках. Удалите сильно пораженные растения. Поливайте под корень. Увеличьте калийные подкормки. Используйте устойчивые гибриды.'
    },
    {
        "disease_name": 'Peach leaf',
        "recommendation": 'Полностью здоровый лист персика.'
    },
    {
        "disease_name": 'Potato leaf early blight',
        "recommendation": 'Опрыскайте ботву медьсодержащими фунгицидами. Увеличьте калийные удобрения. Регулярно окучивайте. Уничтожайте ботву перед уборкой. Соблюдайте севооборот.'
    },
    {
        "disease_name": 'Potato leaf late blight',
        "recommendation": 'Немедленно обработайте фунгицидами против фитофторы. Повторите обработку. Скосите ботву перед уборкой. Просушите клубни. Используйте здоровый посадочный материал.'
    },
    {
        "disease_name": 'Potato leaf',
        "recommendation": 'Полностью здоровый лист картофеля.'
    },
    {
        "disease_name": 'Raspberry leaf',
        "recommendation": 'Полностью здоровый лист малины.'
    },
    {
        "disease_name": 'Soyabean leaf',
        "recommendation": 'Полностью здоровый лист сои.'
    },
    {
        "disease_name": 'Soybean leaf',
        "recommendation": 'Полностью здоровый лист сои.'
    },
    {
        "disease_name": 'Squash Powdery mildew leaf',
        "recommendation": 'Обработайте «Фитоспорином» или коллоидной серой. Удалите сильно пораженные листья. Нормализуйте полив. Обеспечьте освещение и проветривание. Подкормите калием.'
    },
    {
        "disease_name": 'Strawberry leaf',
        "recommendation": 'Полностью здоровый лист земляники садовой (клубники).'
    },
    {
        "disease_name": 'Tomato Early blight leaf',
        "recommendation": 'Удалите нижние пораженные листья. Обработайте медьсодержащим фунгицидом. Мульчируйте почву. Проветривайте теплицу. Подкормите калиевой селитрой.'
    },
    {
        "disease_name": 'Tomato Septoria leaf spot',
        "recommendation": 'Удалите листья с белыми пятнами. Обработайте бордосской смесью. Избегайте загущенных посадок. Поливайте под корень. Соблюдайте севооборот.'
    },
    {
        "disease_name": 'Tomato leaf bacterial spot',
        "recommendation": 'Удалите сильно пораженные растения. Используйте медьсодержащие бактерициды. Дезинфицируйте инструмент. Избегайте верхнего полива. Используйте протравленные семена.'
    },
    {
        "disease_name": 'Tomato leaf late blight',
        "recommendation": 'Обработайте фунгицидом против фитофторы. Повторите обработку. Удалите пасынки и нижние листья. Прекратите полив. Сильно пораженные растения сожгите.'
    },
    {
        "disease_name": 'Tomato leaf mosaic virus',
        "recommendation": 'Больное растение выкопайте и сожгите. Боритесь с тлей. Дезинфицируйте инструмент. Не используйте семена от больных растений. Сажайте устойчивые гибриды.'
    },
    {
        "disease_name": 'Tomato leaf yellow virus',
        "recommendation": 'Удалите растение с вирусом. Установите ловушки для белокрылки. Обрабатывайте инсектицидами. Используйте устойчивые сорта. Уничтожайте сорняки.'
    },
    {
        "disease_name": 'Tomato leaf',
        "recommendation": 'Полностью здоровый лист томата.'
    },
    {
        "disease_name": 'Tomato mold leaf',
        "recommendation": 'Удалите заплесневелые листья. Улучшите вентиляцию, сократите полив. Обработайте «Триходермином». Избегайте перепадов температур. Мульчируйте почву.'
    },
    {
        "disease_name": 'Tomato two spotted spider mites leaf',
        "recommendation": 'Обработайте акарицидом с обеих сторон листьев. Обрежьте зараженные листья. Уничтожьте сорняки. Осенью продезинфицируйте теплицу серной шашкой.'
    },
    {
        "disease_name": 'grape leaf black rot',
        "recommendation": 'Удалите пораженные листья и грозди. Обеспечьте проветриваемость куста. Обработайте фунгицидами на основе манкоцеба. Проведите искореняющую обработку осенью. Сожгите опавшие листья.'
    },
    {
        "disease_name": 'grape leaf',
        "recommendation": 'Полностью здоровый лист винограда.'
    }
]


def upgrade() -> None:
    
    diseases_table = table(
        'diseases', 
        column('disease_name', sa.String),
        column('recommendation', sa.String)
    )

    # Производим массовую вставку данных
    op.bulk_insert(diseases_table, disease_data)


def downgrade() -> None:
    # ОТКАТ: Удаляем вставленные данные по их именам
    names_to_delete = [item["disease_name"] for item in disease_data]
    
    # Используем op.execute с параметрами для безопасности
    op.execute(
        sa.text("DELETE FROM diseases WHERE disease_name IN :names"),
        names=tuple(names_to_delete)
    )