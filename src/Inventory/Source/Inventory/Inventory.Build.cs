// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Inventory : ModuleRules
{
	public Inventory(ReadOnlyTargetRules Target) : base(Target)
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
			"Inventory",
			"Inventory/Variant_Platforming",
			"Inventory/Variant_Platforming/Animation",
			"Inventory/Variant_Combat",
			"Inventory/Variant_Combat/AI",
			"Inventory/Variant_Combat/Animation",
			"Inventory/Variant_Combat/Gameplay",
			"Inventory/Variant_Combat/Interfaces",
			"Inventory/Variant_Combat/UI",
			"Inventory/Variant_SideScrolling",
			"Inventory/Variant_SideScrolling/AI",
			"Inventory/Variant_SideScrolling/Gameplay",
			"Inventory/Variant_SideScrolling/Interfaces",
			"Inventory/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
