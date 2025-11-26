"""insert_initial_diseases

Revision ID: 890f13245e0d
Revises: fa2e08326c7e
Create Date: 2025-11-26 16:58:53.790094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

DISEASES_DATA = [
    {
        "disease_name": "Apple Scab Leaf",
        "recommendation": "Удалите и сожгите пораженные листья и плоды. Обрабатывайте медьсодержащими фунгицидами до и после цветения. Осенью уничтожьте растительные остатки. Проводите прореживающую обрезку для вентиляции. Выбирайте устойчивые сорта."
    },
    {
        "disease_name": "Apple leaf",
        "recommendation": "Полностью здоровый лист яблони."
    },
    {
        "disease_name": "Apple rust leaf",
        "recommendation": "Удалите листья с оранжевыми пятнами. Не сажайте рядом с можжевельником. Обработайте медьсодержащими фунгицидами после цветения. Осенью перекопайте приствольный круг. Весной используйте бордосскую жидкость."
    },
    {
        "disease_name": "Bell_pepper leaf spot",
        "recommendation": "Удалите больные листья, обеспечьте вентиляцию. Поливайте только под корень. Обработайте «Фитоспорином» или медьсодержащими препаратами. Мульчируйте почву. Соблюдайте севооборот."
    },
    {
        "disease_name": "Bell_pepper leaf",
        "recommendation": "Полностью здоровый лист болгарского перца."
    },
    {
        "disease_name": "Blueberry leaf",
        "recommendation": "Полностью здоровый лист голубики."
    },
    {
        "disease_name": "Cherry leaf",
        "recommendation": "Полностью здоровый лист вишни."
    },
    {
        "disease_name": "Corn Gray leaf spot",
        "recommendation": "Соблюдайте севооборот. Используйте устойчивые гибриды. Уничтожайте послеуборочные остатки. Применяйте фунгициды при вспышке. Избегайте густых посевов."
    },
    {
        "disease_name": "Corn leaf blight",
        "recommendation": "Уничтожьте зараженные остатки после урожая. Выбирайте устойчивые гибриды. Обеспечьте пространство для проветривания. Обработайте фунгицидом при первых признаках. Сбалансируйте подкормки."
    },
    {
        "disease_name": "Corn rust leaf",
        "recommendation": "Обработайте фунгицидом при первых признаках. Удалите сильно пораженные растения. Поливайте под корень. Увеличьте калийные подкормки. Используйте устойчивые гибриды."
    },
    {
        "disease_name": "Peach leaf",
        "recommendation": "Полностью здоровый лист персика."
    },
    {
        "disease_name": "Potato leaf early blight",
        "recommendation": "Опрыскайте ботву медьсодержащими фунгицидами. Увеличьте калийные удобрения. Регулярно окучивайте. Уничтожайте ботву перед уборкой. Соблюдайте севооборот."
    },
    {
        "disease_name": "Potato leaf late blight",
        "recommendation": "Немедленно обработайте фунгицидами против фитофторы. Повторите обработку. Скосите ботву перед уборкой. Просушите клубни. Используйте здоровый посадочный материал."
    },
    {
        "disease_name": "Potato leaf",
        "recommendation": "Полностью здоровый лист картофеля."
    },
    {
        "disease_name": "Raspberry leaf",
        "recommendation": "Полностью здоровый лист малины."
    },
    {
        "disease_name": "Soyabean leaf",
        "recommendation": "Полностью здоровый лист сои."
    },
    {
        "disease_name": "Soybean leaf",
        "recommendation": "Полностью здоровый лист сои."
    },
    {
        "disease_name": "Squash Powdery mildew leaf",
        "recommendation": "Обработайте «Фитоспорином» или коллоидной серой. Удалите сильно пораженные листья. Нормализуйте полив. Обеспечьте освещение и проветривание. Подкормите калием."
    },
    {
        "disease_name": "Strawberry leaf",
        "recommendation": "Полностью здоровый лист земляники садовой (клубники)."
    },
    {
        "disease_name": "Tomato Early blight leaf",
        "recommendation": "Удалите нижние пораженные листья. Обработайте медьсодержащим фунгицидом. Мульчируйте почву. Проветривайте теплицу. Подкормите калиевой селитрой."
    },
    {
        "disease_name": "Tomato Septoria leaf spot",
        "recommendation": "Удалите листья с белыми пятнами. Обработайте бордосской смесью. Избегайте загущенных посадок. Поливайте под корень. Соблюдайте севооборот."
    },
    {
        "disease_name": "Tomato leaf bacterial spot",
        "recommendation": "Удалите сильно пораженные растения. Используйте медьсодержащие бактерициды. Дезинфицируйте инструмент. Избегайте верхнего полива. Используйте протравленные семена."
    },
    {
        "disease_name": "Tomato leaf late blight",
        "recommendation": "Обработайте фунгицидом против фитофторы. Повторите обработку. Удалите пасынки и нижние листья. Прекратите полив. Сильно пораженные растения сожгите."
    },
    {
        "disease_name": "Tomato leaf mosaic virus",
        "recommendation": "Больное растение выкопайте и сожгите. Боритесь с тлей. Дезинфицируйте инструмент. Не используйте семена от больных растений. Сажайте устойчивые гибриды."
    },
    {
        "disease_name": "Tomato leaf yellow virus",
        "recommendation": "Удалите растение с вирусом. Установите ловушки для белокрылки. Обрабатывайте инсектицидами. Используйте устойчивые сорта. Уничтожайте сорняки."
    },
    {
        "disease_name": "Tomato leaf",
        "recommendation": "Полностью здоровый лист томата."
    },
    {
        "disease_name": "Tomato mold leaf",
        "recommendation": "Удалите заплесневелые листья. Улучшите вентиляцию, сократите полив. Обработайте «Триходермином». Избегайте перепадов температур. Мульчируйте почву."
    },
    {
        "disease_name": "Tomato two spotted spider mites leaf",
        "recommendation": "Обработайте акарицидом с обеих сторон листьев. Обрежьте зараженные листья. Уничтожьте сорняки. Осенью продезинфицируйте теплицу серной шашкой."
    },
    {
        "disease_name": "grape leaf black rot",
        "recommendation": "Удалите пораженные листья и грозди. Обеспечьте проветриваемость куста. Обработайте фунгицидами на основе манкоцеба. Проведите искореняющую обработку осенью. Сожгите опавшие листья."
    },
    {
        "disease_name": "grape leaf",
        "recommendation": "Полностью здоровый лист винограда."
    }
]

# revision identifiers, used by Alembic.
revision: str = '890f13245e0d'
down_revision: Union[str, Sequence[str], None] = 'fa2e08326c7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    disease_table = sa.table('diseases',
                             sa.column("disease_name", sa.String(50)),
                             sa.column("recommendation", sa.Text())
                             )
    op.bulk_insert(disease_table, DISEASES_DATA)
    print("Data inserted successfully")


def downgrade() -> None:
    op.execute("DELETE FROM diseases")
    print("Data removed")
