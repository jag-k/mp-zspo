from pony.orm.migrations.operations import AddRelation
from pony.orm.migrations.virtuals import Set, Optional

dependencies = [
    '00000_initial'
]

operations = [
    AddRelation(entity1_name='Post', attr1=Optional('category', 'Category'), entity2_name='Category', attr2=Set('posts', 'Post', cascade_delete=True)),

    AddRelation(entity1_name='Post', attr1=Optional('header', 'Header', cascade_delete=True), entity2_name='Header', attr2=Optional('post', 'Post')),

    AddRelation(entity1_name='Category', attr1=Optional('block', 'Block'), entity2_name='Block', attr2=Set('categories', 'Category', cascade_delete=True))
]
