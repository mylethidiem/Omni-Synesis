// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class InventoryProject : ModuleRules
{
	public InventoryProject(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"InventoryProject",
			"InventoryProject/Variant_Platforming",
			"InventoryProject/Variant_Platforming/Animation",
			"InventoryProject/Variant_Combat",
			"InventoryProject/Variant_Combat/AI",
			"InventoryProject/Variant_Combat/Animation",
			"InventoryProject/Variant_Combat/Gameplay",
			"InventoryProject/Variant_Combat/Interfaces",
			"InventoryProject/Variant_Combat/UI",
			"InventoryProject/Variant_SideScrolling",
			"InventoryProject/Variant_SideScrolling/AI",
			"InventoryProject/Variant_SideScrolling/Gameplay",
			"InventoryProject/Variant_SideScrolling/Interfaces",
			"InventoryProject/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
