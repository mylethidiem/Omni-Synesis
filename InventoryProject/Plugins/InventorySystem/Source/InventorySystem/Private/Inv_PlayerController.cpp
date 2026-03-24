


#include "Inv_PlayerController.h"
#include "InventorySystem.h"

void AInv_PlayerController::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogInventory, Log, TEXT("Let's begin to play Inventory Game!"))
}
