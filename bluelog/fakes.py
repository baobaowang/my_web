#生成虚拟数据

#生成虚拟管理员信息
from bluelog.models import Admin 
from bluelog.extensions import db
def fake_admin():
    admin = Admin(
        username = 'admin',
        blog_title = 'Bluelog',
        blog_sub_title="No, I'm the real thing.",
        name = 'Mima Kirigoe',
        about = 'Un,Mima Kirigos, had a fun time as a member of CHAM...'
    )
    db.session.add(admin)
    db.session.commit()


#创建虚拟分类
from faker import Faker
from bluelog.models import Category
from bluelog.extensions import db
fake = Faker()

def fake_categories(count = 10):
    category = Category(name = 'Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name = fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


#生成虚拟文章
from faker import Faker
import random#随机数
from bluelog.models import Post
from bluelog.extensions import db
fake = Faker()
def fake_posts(count = 50):
    for i in range(count):
        post = Post(
            title = fake.sentence(),
            body = fake.text(2000),
            category = Category.query.get(random.randint(1,Category.query.count()   ))
            timestamp = fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

#生成虚拟评论
from faker import Faker
from bluelog.models import Comment
from bluelog.extensions import db























