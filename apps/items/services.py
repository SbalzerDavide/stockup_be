import dataclasses
import datetime
import httpx

from langchain_core.prompts import ChatPromptTemplate

from typing import TYPE_CHECKING, Annotated, TypedDict

from .models import Items

from apps.item_categories import services as model_categorires

import os
from dotenv import load_dotenv
# Carica le variabili dal file .env
load_dotenv()



from apps.llm.models import llm


if TYPE_CHECKING:
  from .models import Items
    

@dataclasses.dataclass
class ItemDataClass:
  name: str
  category: str = None
  consumation_average_days: float = None
  department: str = None
  is_edible: bool = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, items_model: "Items") -> "ItemDataClass":
    return cls(
      id=items_model.id,
      name=items_model.name,
      category=items_model.category,
      consumation_average_days=items_model.consumation_average_days,
      department=items_model.department,
      is_edible=items_model.is_edible,
      created_at=items_model.created_at,
      updated_at=items_model.updated_at
    )    
    
def create_item(user, item_dc: "ItemDataClass") -> "ItemDataClass":
  proposed_category = autoSetCategory(name=item_dc.name, user=user)
  print(proposed_category)
  items_create = Items.objects.create(
    name=item_dc.name,
    consumation_average_days=item_dc.consumation_average_days,
    department=proposed_category,
    is_edible=item_dc.is_edible,
    category=item_dc.category,
    user=user
  )
  return ItemDataClass.from_instance(items_create)

class predictedCategory(TypedDict):
    category: Annotated[str, ..., "La categorie del prodotto"]


def autoSetCategory(name: str, user) -> str:
  categories = model_categorires.get_item_categories(user)
  category_names = [category.name for category in categories]
  separetor = ', '
  categories_string = separetor.join(map(str, category_names))
  prompt = ChatPromptTemplate.from_messages([
      ("system", "Devi catalogare prodotti che puoi trovare in un supermercato"),
      ("user", f"Tra le categorie: {categories_string}. A quale appartiene {name}?"),
  ])
  # prompt = ChatPromptTemplate.from_messages([
  #   ("system", "You are a world class technical documentation writer."),
  #   ("user", "{input}")
  # ])
  structured_llm = llm.with_structured_output(predictedCategory)
  chain = prompt | structured_llm 
  print("---------------")
  # print(chain.invoke({"input": "how can langsmith help with testing?"}))
  print(chain.invoke({"input": 'prompt'}))
  print (prompt)
  proposed_category = chain.invoke({"input": 'prompt'})['category']
  return proposed_category
  
